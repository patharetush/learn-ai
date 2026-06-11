from langchain_core.runnables import RunnableLambda
from typing import cast
import asyncio

"""
# Demo - Lambda Function
runnable_multiply = RunnableLambda(lambda x: cast(int, x) * 10)

invoke_result = runnable_multiply.invoke(3)

print(invoke_result)

batch_results = runnable_multiply.batch([3, 7, 5])
for result in batch_results:
    print(result)

"""

# Demo 2- regular function to Lambda function
def reverse_text_func(text: str) -> str:
    return text[::-1]

reverse_text_runnable = RunnableLambda(reverse_text_func)

"""
text_invoke_result = reverse_text_runnable.invoke("Tushar")
print(text_invoke_result)

text_batch_result = reverse_text_runnable.batch(["Banana", "Apple", "Grapes"])
for result in text_batch_result:
    print(result)
"""

batch_async_inputs = [
    "Inception",
    "The Dark Knight"
    "Interstellar"
    "Avengers: Endgame"
]

async def run_async():
    # result = await reverse_text_runnable.ainvoke("I love my Country")
    # print(result)
    aresult = await reverse_text_runnable.abatch(batch_async_inputs)
    print(aresult)

asyncio.run(run_async())