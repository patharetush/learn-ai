from openai import OpenAI

client = OpenAI()

first_response = client.responses.create(
    model="gpt-5.5",
    input="Find the shipping ETA tool first, then use it for order_42.",
    tools=[
        {
            "type": "tool_search",
            "execution": "client",
            "description": "Find the project-specific tools needed to continue the task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal": {"type": "string"},
                },
                "required": ["goal"],
                "additionalProperties": False,
            },
        }
    ],
    parallel_tool_calls=False,
)

print("=" * 60)
print("first_response.output:")
print(first_response.output)
print("=" * 60)


search_call = next(
    (item for item in first_response.output
     if item.type == "tool_search_call"),
    None
)


if search_call is None:
    raise ValueError("No tool_search_call found in the response.")

loaded_tools = [
    {
        "type": "function",
        "name": "get_shipping_eta",
        "description": "Look up shipping ETA details for an order.",
        "defer_loading": True,
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
    }
]

second_response = client.responses.create(
    model="gpt-5.5",
    input=[
        *first_response.output,
        {
            "type": "tool_search_output",
            "execution": "client",
            "call_id": search_call.call_id,
            "status": "completed",
            "tools": loaded_tools,
        },
    ],
)

print("=" * 60)
print("second_response.output:")
print(second_response.output)
print("=" * 60)