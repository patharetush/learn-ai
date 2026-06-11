from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import  HumanMessage

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def chatbot(state: MessagesState) -> MessagesState:
    response = llm.invoke(state["messages"])
    return {
        "messages": [response]
    }

builder = StateGraph(MessagesState)
builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

checkpointer = MemorySaver()

graph = builder.compile()
#graph = builder.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "chat_session_1"
    }
}

# Turn 1: User sends a message to the chatbot
message1 = "Hi, my name is Alice. I'm a engineer"

input1 = {
    "messages": [HumanMessage(content=message1)]
}

result1 = graph.invoke(input1, config=config)
print(f"User: {message1}")
print(f"Assistant: {result1['messages'][-1].content}")

# Turn 2: User asks the chatbot to recall their name
message2 = "What is my name?"

input2 = {
    "messages": [HumanMessage(content=message2)]
}

result2 = graph.invoke(input2, config=config)
print(f"User: {message2}")
print(f"Assistant: {result2['messages'][-1].content}")