from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1-nano")

response = model.invoke("Who is presient of France?")

print(response.content)