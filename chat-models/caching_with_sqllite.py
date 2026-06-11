from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

set_llm_cache(SQLiteCache(database_path="cached_responses.db"))

prompt = "Who is president of Germany"
response1 = model.invoke(prompt)
print(response1.content)

response2 = model.invoke(prompt)
print(response2.content)