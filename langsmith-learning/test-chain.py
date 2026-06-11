from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Tell me a joke about {topic}"
)

model = ChatOpenAI(model="gpt-4o-mini")

chain = prompt | model

result = chain.invoke({
    "topic": "AI Programming"
})

print(result.content)