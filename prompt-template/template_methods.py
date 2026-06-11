from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Who is the {role} of {country}?")

invoked_prompt = prompt_template.invoke({
    "role": "President",
    "country": "India"
})

print(prompt_template)
print(invoked_prompt)

formatted_prompt = prompt_template.format(role="Prime Minister",  country= "India")
print(formatted_prompt)

formatted_prompt = prompt_template.format_prompt(role="Prime Minister",  country= "India")
print(formatted_prompt)

batched_prompts = prompt_template.batch([
    {"role": "Prime Minister", "country": "India"},
    {"role": "President", "country": "India"},
    {"role": "King", "country": "United Kingdom"},
])

print(batched_prompts)

prompt_template.pretty_print()

prompt_template.save("my_prompt_template.yml")