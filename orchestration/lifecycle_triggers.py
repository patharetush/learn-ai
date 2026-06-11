from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers.schemas import Run

#1. LLM Setup (simple initialization)
model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("Give me a very short, simple fact about {topic}")
fact_chain = prompt | model | StrOutputParser()

def my_listener_on_start(run: Run):
    """ Logs when the chain start, accessig the data from Run object"""
    print(f"Listener start for '{run.name} (Run ID: {run.id})")
    print(f"Inputs: {run.inputs}")
    print(f"Parrent Run ID: {run.parent_run_id}")
    print(f"Tags: {run.tags}, Metadata: {run.extra.get("metadata")}")

def my_listener_on_end(run: Run):
    """ Logs when the chain ends, accessig the data from Run object"""
    print(f"Listener end for '{run.name} (Run ID: {run.id})")
    print(f"Output Type: {type(run.outputs).__name__}, Output Values: {run.outputs}")
    print(f"Parrent Run ID: {run.parent_run_id}")
    print(f"Tags: {run.tags}, Metadata: {run.extra.get('metadata')}") 

fact_chain_with_listener = fact_chain.with_listeners(
    on_start=my_listener_on_start,
    on_end=my_listener_on_end
)

result = fact_chain_with_listener.invoke({
    "topic": "The Eiffel Tower"
})

print(f"Final result is: {result}")
print("="* 50)