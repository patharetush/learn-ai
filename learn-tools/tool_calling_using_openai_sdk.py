import asyncio

from agents import Agent
from agents import Runner
from agents import function_tool


# -----------------------------
# Tool 1
# -----------------------------
@function_tool
def get_customer(email: str) -> dict:
    """
    Find customer information by email.
    """

    customers = {
        "john@example.com": {
            "customer_id": 101,
            "name": "John Smith",
            "tier": "Gold",
        }
    }

    return customers.get(email, {"error": "Customer not found"})


# -----------------------------
# Tool 2
# -----------------------------
@function_tool
def get_orders(customer_id: int) -> list:
    """
    Return recent customer orders.
    """

    orders = {
        101: [
            {
                "order_id": "ORD-1001",
                "amount": 299.99,
                "status": "Delivered",
            },
            {
                "order_id": "ORD-1002",
                "amount": 149.99,
                "status": "Processing",
            },
        ]
    }

    return orders.get(customer_id, [])


# -----------------------------
# Tool 3
# -----------------------------
@function_tool
def get_account_balance(customer_id: int) -> dict:
    """
    Return outstanding balance.
    """

    balances = {
        101: {
            "outstanding_balance": 120.50,
            "currency": "USD",
        }
    }

    return balances.get(customer_id, {})


# -----------------------------
# Agent
# -----------------------------
MODEL_NAME = "gpt-4.1-nano"

agent = Agent(
    name="Customer Support Agent",
    model=MODEL_NAME,
    instructions="""
You are a customer support assistant.

When a customer email is provided:

1. First find the customer.
2. Retrieve their recent orders.
3. Retrieve their account balance.
4. Provide a concise summary.

Use tools whenever information is required.
""",
    tools=[
        get_customer,
        get_orders,
        get_account_balance,
    ],
)

#-----------------------------
# Log the token usage for transparency
#-----------------------------
def log_token_usage(result, model_name: str):
    total_requests = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0

    print("\n=== Token Usage Details ===")

    for idx, resp in enumerate(result.raw_responses, start=1):
        usage = resp.usage

        print(
            f"LLM Call #{idx}: "
            f"input={usage.input_tokens}, "
            f"output={usage.output_tokens}, "
            f"total={usage.total_tokens}"
        )

        total_requests += usage.requests
        total_input_tokens += usage.input_tokens
        total_output_tokens += usage.output_tokens
        total_tokens += usage.total_tokens

    print("\n=== Aggregated Usage ===")
    print(f"Model         : {model_name}")
    print(f"Requests      : {total_requests}")
    print(f"Input Tokens  : {total_input_tokens}")
    print(f"Output Tokens : {total_output_tokens}")
    print(f"Total Tokens  : {total_tokens}")

    return {
        "model": model_name,
        "requests": total_requests,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_tokens,
    }

# -----------------------------
# Run
# -----------------------------
async def main():

    result = await Runner.run(
        agent,
        """
        Please check customer john@example.com.
        Tell me:

        - customer tier
        - recent orders
        - outstanding balance
        """
    )

    print(result.final_output)
    log_token_usage(result, MODEL_NAME)


asyncio.run(main())