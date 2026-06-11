from langchain_core.prompts import ChatPromptTemplate

messages = [
    ("system", "you are a helpful assistant that gives straight-forward answers"),
    ("human", "Who is president of {country}"),
    ("ai", "{answer}"),
    ("human", "Who is president of USA")
]

chat_prompt = ChatPromptTemplate(messages)

print(chat_prompt.invoke({
    "country": "INDIA",
    "answer": "Droupadi Murmu",
}).to_string())