from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

example_formatter = PromptTemplate.from_template("Question: {question} " \
                                                "\n {answer}")

example_set = [
    {
        "question": "What is the capital of France?",
        "answer": "The capital of France is Paris.",
        "language": "English"
    },
    {
        "question": "¿Cuál es la capital de Japón?",
        "answer": "La capital de Japón es Tokio.",
        "language": "Spanish"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "answer": "Jupiter is the largest planet in our solar system.",
        "language": "English"
    },
    {
        "question": "भारत की राजधानी क्या है?",
        "answer": "भारत की राजधानी नई दिल्ली है।",
        "language": "Hindi"
    },
    {
        "question": "Who developed the theory of relativity?",
        "answer": "Albert Einstein developed the theory of relativity.",
        "language": "English"
    }
]

fewshot_prompt_template = FewShotPromptTemplate(
    example_prompt = example_formatter,
    examples = example_set,
    suffix="Question: {user_query}"
)

invoked_template = fewshot_prompt_template.invoke({
    "user_query" : "What is the largest planet in our solar system?"
})

print(invoked_template.to_string())