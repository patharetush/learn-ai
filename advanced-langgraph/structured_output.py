from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field
from typing import List
import json

class ProductReview(BaseModel):
    """A structured output model for product reviews"""
    product_name: str = Field(..., description="The name of the product")
    rating: int = Field(..., description="The rating of the product (1-5)", ge=1, le=5)
    review: str = Field(..., description="The review text for the product")

llm = ChatOpenAI(model="gpt-4o", temperature=0)

structured_llm = llm.with_structured_output(ProductReview)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that provides structured product reviews."),
    ("user", "{review_text}")
])

chain = prompt | structured_llm

review_text = """
I recently bought the XYZ headphones.
They have great sound quality but are a bit uncomfortable to wear for long periods.
I would give them 4 out of 5 stars."""

response = chain.invoke({"review_text": review_text})

print("Structured Output:")
print(json.dumps(response.model_dump(), indent=2))


