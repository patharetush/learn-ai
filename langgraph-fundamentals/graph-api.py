from langgraph.graph import StateGraph, START, END
from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages

#1. Define States
class SimpleState(TypedDict):
    messages: Annotated[list, add_messages]

graph = StateGraph(SimpleState)

#2. Create Nodes
def say_hello(state: SimpleState):
    print("Executing 'say hello' node.")
    return {
        "messages": ["Hello"]
    }

def say_world(state: SimpleState):
    print("Executing 'say world' node.")
    return {
        "messages": ["World"]
    }

graph.add_node("hello_node", say_hello)
graph.add_node("world_node", say_world)

#3. Link Nodes with edges
# START -> hello_node -> world_node -> END
graph.add_edge(START, "hello_node")
graph.add_edge("hello_node", "world_node")
graph.add_edge("world_node", END)

#4. Compile Graph
agent = graph.compile()
print(agent.get_graph().draw_ascii())

#5. Run Graph
initial_state = {
    "messages": []
}

final_state = agent.invoke(initial_state)

print(f"\n----- Final State ----")
print(final_state)