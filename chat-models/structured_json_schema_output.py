from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

president_schema = {
    "name": "president_information_schema",
    "description": "Schema for extracting information about the president",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the president"
            },
            "country": {
                "type": "string",
                "description": "The country the president governs"
            },
            "age": {
                "type": "integer",
                "description": "The age of the president"
            },
            "term_start": {
                "type": "string",
                "description": "The start date of the president's term"
            },
            "term_end": {
                "type": "string",
                "description": "The end date of the president's term, if applicable"
            }
        }, 
        "required": ["name", "country", "age"]
    }
}

structured_response = model.with_structured_output(president_schema).invoke("Who is the president of India?")
print(structured_response)