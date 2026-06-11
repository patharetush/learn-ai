from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("Write a short, concise sentence about {topic}")

output_parser = StrOutputParser()

simple_chain = prompt | model | output_parser

result_1 = simple_chain.invoke({
    "topic": "Functional Programing"
})

print(result_1)

# Demo 2 - Chain to Runnable
combined_chain = simple_chain | (lambda chain_output: chain_output + "Oh, wow, that's awesome")
combined_chain_result = combined_chain.invoke({
    "topic": "Platform Architect"
})

print("--------- Combined Chain Output-------------")
print(combined_chain_result)
print("="* 50)

# Demo 3 - Chain to Chain
fact_checking_prompt = ChatPromptTemplate.from_messages([
    ("system", "Start by quoating the statement, then give the reason"),
    ("user", "How correct is this statement: {statement}")
])

checker_chain = fact_checking_prompt | model | output_parser
fact_checking_chain  = {"statement": simple_chain} | checker_chain

dual_chain_result = fact_checking_chain.invoke({
    "topic" : "Prompt Engineering"
})

print("--------- Dual Chain Output-------------")
print(dual_chain_result)
print("="* 50)

