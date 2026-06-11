from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback

model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

with get_openai_callback() as callback:
    response = model.invoke("Describe the NFL")
    response = model.invoke("Who is CEO of OpenAI")
    print(callback)
    #print(callback.total_cost)