from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1-nano")

response = model.invoke("Who is presient of India?")

#print(response.usage_metadata)
print(response.response_metadata["token_usage"])