from langchain.agents import create_agent
from langchain.tools import tool,ToolRuntime
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: str
    user_name: str
    membership_tier: str # basic, premium, platinum
    preferred_currency: str

USER_DATABASE = {
    "user_001": {
        "name": "Alice Johnson",
        "accounts": {
            "checking": 2500.00,
            "savings": 15000.00,
            "investment": 45000.00,
        },
        "transactions": {
            "checking": [
                {"date": "2025-01-15", "description": "Grocery Store", "amount": -85.50},
                {"date": "2025-01-14", "description": "Direct Deposit", "amount": 3200.00},
                {"date": "2025-01-13", "description": "Electric Bill", "amount": -120.00},
                {"date": "2025-01-12", "description": "Restaurant", "amount": -45.00},
                {"date": "2025-01-10", "description": "Gas Station", "amount": -55.00},
            ],
            "savings": [
                {"date": "2025-01-01", "description": "Interest Payment", "amount": 12.50},
                {"date": "2024-12-15", "description": "Transfer from Checking", "amount": 500.00},
            ],
            "investment": [
                {"date": "2025-01-14", "description": "Dividend - AAPL", "amount": 125.00},
                {"date": "2025-01-10", "description": "Buy - VTI", "amount": -1000.00},
            ],
        },
    },
    "user_002": {
        "name": "Bob Smith",
        "accounts": {
            "checking": 1200.00,
            "savings": 8000.00,
            "investment": 22000.00,
        },
        "transactions": {
            "checking": [
                {"date": "2025-01-15", "description": "Coffee Shop", "amount": -5.50},
                {"date": "2025-01-14", "description": "Freelance Payment", "amount": 1500.00},
            ],
            "savings": [
                {"date": "2025-01-01", "description": "Interest Payment", "amount": 6.50},
            ],
            "investment": [
                {"date": "2025-01-12", "description": "Dividend - VTI", "amount": 45.00},
            ],
        },
    },
}

@tool
def get_account_balance(account_type: str, runtime: ToolRuntime[UserContext]) -> str:
    """
        Get the current balance for a specific account for a user

        Args:
            account_type: Type of account - 'checking', 'savings', or 'investment'
    """

    user_id = runtime.context.user_id
    currency = runtime.context.preferred_currency
    user_data = USER_DATABASE.get(user_id, {})

    balance = user_data.get("accounts", {}).get(account_type.lower())

    if balance is not None:
        if currency == "EUR":
            balance = balance * 0.92 
            return f"Your {account_type} account balance is €{balance:,.2f}"
        return f"Your {account_type} account balance is ${balance:,.2f}"
    
    return f"Unknown account type: {account_type}. Available: checking, savings, investment"


@tool
def get_recent_transactions(
    account_type: str, 
    limit: int = 5,
    runtime: ToolRuntime[UserContext] = None
    ) -> str:

    """
        Get recent transactions for an account of a user

        Args:
         account_type: Type of account - savings, investment, checking
         limit: Number of transactions to return (default: 5)
    """

    
    user_id = runtime.context.user_id
    user_data = USER_DATABASE.get(user_id, {})

    account_transactions = user_data.get("transactions", {}).get(account_type.lower(), [])[:limit]

    if not account_transactions:
        return f"No transactions found for {account_type}"
    
    result = f"Recent transactions for {account_type}:\n"

    for t in account_transactions:
        sign = "+" if t["amount"] > 0 else ""
        result += f"{t['date']}: {t['description']} ({sign}${t['amount']:,.2f})\n"

    return result

@tool
def calculate_budget(monthly_income: float, expense_category: str) -> str:
    
    """
        Calaculate recommended budget allocation for an expense category

        Args:
            monthly_income: User's monthly income
            expense_category: Categories like 'housing', 'food' etc
    """

    allocations = {
        "housing": 0.30,
        "food": 0.12,
        "transportation": 0.10,
        "utilities": 0.08,
        "savings": 0.20,
        "entertainment": 0.05,
        "healthcare": 0.05,
        "other": 0.10,
    }

    percentage = allocations.get(expense_category.lower())
    if percentage is None:
        return f"Unknown category: {expense_category}. Available {', '.join(allocations.keys())}"
    
    recommended = monthly_income * percentage

    return f"Recommended {expense_category} budget: ${recommended:,.2f}/month ({percentage*100:.0f}% of income)"

@tool
def get_personalized_greeting(runtime: ToolRuntime[UserContext]) -> str:
    """
        Get a personalized greeting for the user. No arguments required
    """

    name = runtime.context.user_name
    tier = runtime.context.membership_tier

    tier_benefits = {
        "basic": "You have access to standard features.",
        "premium": "As a premium member, you get priority support and advanced analytics!",
        "platinum": "Welcome, platinum member! You have access to all features including personal advisor consultations.",
    }

    benefit_msg = tier_benefits.get(tier, "")
    return f"Hello, {name}! {benefit_msg}"

SYSTEM_PROMPT = """
You are a helpful personal finance assistant.

Your capabilities:
- Check account balances (checking, savings, investment)
- View recent transactions
- Calculate budget recommendations
- Provide personalized greetings

Guidelines:
- Be helpful and informative
- Always start by greeting the user 
- Provide clear, actionable advice
- Use tools to get accurate, user-specific information
- Format monetary values clearly
- Tailor advice based on the user's membership tier
"""


agent = create_agent(
    model="gpt-4o-mini",
    tools=[
        get_account_balance,
        get_recent_transactions,
        calculate_budget,
        get_personalized_greeting
    ],
    system_prompt=SYSTEM_PROMPT,
    context_schema=UserContext
)


def main():
    print("=" * 60)
    print("Stage 1: Simple Finance Assistant")
    print("=" * 60)

    alice_context = UserContext(
        user_id= "user_001",
        user_name= "Alice Johnson",
        membership_tier= "platinium",
        preferred_currency= "USD"
    )

    bob_context = UserContext(
        user_id= "user_001",
        user_name= "Bob Smith",
        membership_tier= "basic",
        preferred_currency= "EUR"
    )

    """
    # Test 1: Check Balance
    query = "What is my checking account balance?"
    print(f"Query: {query}")
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]},
        context= alice_context
    )

    print("\nAssistant:")
    print(response["messages"][-1].content)
    """
    
    # Test 2: Multitool query
    query = "Show my savings balance and recent transactions"
    print(f"Query: {query}")
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]},
        context= bob_context
    )

    print("\nAssistant:")
    print(response["messages"][-1].content)
    

if __name__ == "__main__":
    main()