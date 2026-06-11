from langchain_core.prompts import PromptTemplate

string_prompt1 = PromptTemplate.from_template("Write a poem about {topic}")

actual_prompt = string_prompt1.invoke({
    "topic": "langchain"
})

print(actual_prompt)