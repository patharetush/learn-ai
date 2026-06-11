from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import  Optional

model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

class President(BaseModel):
    """Details about the president """
    name: str = Field(description="Name of the president")
    coutry: str = Field(description="Country of the president")
    age: Optional[int] = Field(default=None, description="Age of the president")

structured_response = model.with_structured_output(President).invoke("Who is the president of India?")
print(structured_response)
