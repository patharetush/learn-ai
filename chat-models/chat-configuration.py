from langchain_openai import ChatOpenAI
import dotenv
import os

dotenv.load_dotenv()

model = ChatOpenAI(model="gpt-4.1-nano", api_key=os.getenv("OPENAI_API_KEY"))
response = model.invoke("Who is president of France?")

print(response.content)