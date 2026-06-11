from langchain_openai import ChatOpenAI
from langchain_core.language_models.base import LanguageModelInput


model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

"""""
# Demo 1 - Invoke
invoked_prompt = "Where is Taj Mahal?"

invoked_response = model.invoke(invoked_prompt)

print(f"------Invoked Prompt - Query: {invoked_prompt}")
print(invoked_response.content)
print("=" * 50)

# Demo 2 - Batch
batch_prompts: list[LanguageModelInput] = [
    "Is Pineapple is fruit or vegetable?",
    "When was the Snow White and the Seven Dwarfs first produced?",
    "Who is strongest wizard in Harry Porter?"
]
batched_response = model.batch(batch_prompts)
print(f"-----Batched Prompt-----")
for response in batched_response:
    print(response.content)
    print("-" * 50)
print("=" * 50)
"""

# Demo 3 - Streaming

stream_promot = "Explain me what is model in llm?"
streamed_response = model.stream(stream_promot)
for chunk in streamed_response:
    print(chunk.content, end="", flush=True)
