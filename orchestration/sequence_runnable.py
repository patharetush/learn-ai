from langchain_core.runnables import RunnableLambda, RunnableSequence
from typing import cast

runnable1 = RunnableLambda(lambda input: cast(int, input) + 10)
runnable2 = RunnableLambda(lambda input: cast(int, input) * 10)
""" 
print("-------- Runnable Sequence -----------")
sequence_1 = RunnableSequence(
    first=runnable1,
    last=runnable2
)

result_1 = sequence_1.invoke(5)
print(result_1)
"""

"""
print("-------- Using Pipes -----------")

sequence_2 = runnable1.pipe(runnable2)
result_2 = sequence_2.invoke(5)
print(result_2)
"""
print("-------- Using LCEL (|) -----------")

sequence_3 = runnable1 | runnable2
result_3 = sequence_3.invoke(5)
print(result_3)

