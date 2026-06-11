from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

set_llm_cache(InMemoryCache())

prompt = "Who is president of Germany"
response1 = model.invoke(prompt)
print(response1.content)

response2 = model.invoke(prompt)
print(response2.content)