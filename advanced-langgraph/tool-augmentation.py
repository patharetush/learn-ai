from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location"""
   
    wheather_data = {
        "New York": "Sunny, 25°C",
        "San Francisco": "Foggy, 15°C",
        "London": "Rainy, 10°C"
    }

    return wheather_data.get(location, "Weather data not available for this location")  

@tool
def calculate_tip(amount: float, percentage: float) -> float:
    """Calculate the tip based on the amount and percentage"""
    return round(amount * (percentage / 100), 2)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

llm_with_tools = llm.bind_tools([
    get_current_weather,
    calculate_tip
])

prompt = "What is the current weather in New York? and how much tip should I leave for a $50 bill at 20%?"

response = llm_with_tools.invoke(prompt)
tools_called = response.tool_calls

result = ""
for tool_call in tools_called:
    if tool_call['name'] == "get_current_weather":
        result += "\n" + get_current_weather.invoke(tool_call['args'])
    elif tool_call['name'] == "calculate_tip":
        result += "\n" + str(calculate_tip.invoke(tool_call['args']))
    else:
        result += "\nUnknown tool called."

print(f"Result: {result}")