from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

example_formatter = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}")
    ])

example_set = [
    {
        "input": "2 ribbit 2",
        "output": "4"
    },
     {
        "input": "5 ribbit 2",
        "output": "10"
    },
     {
        "input": "2 ribbit 10",
        "output": "20"
    }
]

fewshot_template = FewShotChatMessagePromptTemplate(
    example_prompt=example_formatter,
    examples = example_set
)

main_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a whimsical mathematician"),
    fewshot_template,
    ("human", "{user_prompt}")
])

# invoked_prompt = main_prompt.invoke({
#     "user_prompt": "5 ribbit 2"
# })

#print(invoked_prompt.to_string())
model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

# formatted_prompt = main_prompt.format(
#     user_prompt = "6 ribbit 10"
# )
# response = model.invoke(formatted_prompt)

# print(response.content)

# LCEL - Langchain Expression Langauge

chain = main_prompt | model

response = chain.invoke({
    "user_prompt": "7 ribbit 2"
})

print(response.content)