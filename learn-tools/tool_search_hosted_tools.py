from openai import OpenAI
import json

client = OpenAI()


# --------------------------
# Actual CRM implementation
# --------------------------

def get_customer_profile(customer_id: str):
    return {
        "customer_id": customer_id,
        "name": "John Doe",
        "email": "john@example.com",
    }


def list_open_orders(customer_id: str):
    return [
        {
            "order_id": "ORD-1001",
            "status": "OPEN",
            "amount": 250.00,
        },
        {
            "order_id": "ORD-1002",
            "status": "OPEN",
            "amount": 175.50,
        },
    ]


# --------------------------
# Namespace definition
# --------------------------

crm_namespace = {
    "type": "namespace",
    "name": "crm",
    "description": "CRM tools for customer lookup and order management.",
    "tools": [
        {
            "type": "function",
            "name": "get_customer_profile",
            "description": "Fetch a customer profile by customer ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                },
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "list_open_orders",
            "description": "List open orders for a customer ID.",
            "defer_loading": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                },
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
    ],
}


# --------------------------
# Initial request
# --------------------------

response = client.responses.create(
    model="gpt-5.5",
    input="List open orders for customer CUST-12345.",
    tools=[
        crm_namespace,
        {"type": "tool_search"},
    ],
)

# --------------------------
# Execute tool calls
# --------------------------

tool_outputs = []

for item in response.output:

    if item.type != "function_call":
        continue

    args = json.loads(item.arguments)

    if item.namespace == "crm":

        if item.name == "get_customer_profile":
            result = get_customer_profile(**args)

        elif item.name == "list_open_orders":
            result = list_open_orders(**args)

        else:
            raise ValueError(f"Unknown tool: {item.name}")

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result),
            }
        )

# --------------------------
# Send tool results back
# --------------------------


final_response = client.responses.create(
    model="gpt-5.4",
    previous_response_id=response.id,
    input=tool_outputs,
)

print(final_response.output_text)