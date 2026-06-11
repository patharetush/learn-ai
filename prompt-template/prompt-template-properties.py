from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

prompt_template = PromptTemplate(
    template="Who is the {role} of {country}?",
    input_variables=["role", "country"],
    input_types= {
        "coutry":str,
        "role": str,
    },
    optional_variables=["gender"],
    validate_template=True
)

print(prompt_template.template)
print(prompt_template.template_format)
print(prompt_template.input_variables)
print(prompt_template.input_types)
print(prompt_template.optional_variables)
print(prompt_template.validate_template)

chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", "You are helpful assistsent"),
        ("human",  "how do I bake {item}"),
    ],
    input_variable = ["item"]
)

print(chat_prompt_template.input_variables)