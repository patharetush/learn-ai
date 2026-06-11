from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda input: str(input).upper())
runnable2 = RunnableLambda(lambda input: str(input).lower())

# Demo 1- Passing dictionary
parallel_1 = RunnableParallel({
    "uppercase": runnable1,
    "lowercase": runnable2
})

result_1 = parallel_1.invoke("The great man")
print(result_1)

# Demo 2 - with keyword arguments
parallel_2 = RunnableParallel(
    first = runnable1,
    second = runnable2
)

result_2 = parallel_2.invoke("Captain America")
print(result_2)

# Demo 3 - with LCEL
print("-------Using LCEL-------")
#parallel_3 = parallel_1 | (lambda dict_int: dict_int['uppercase'] + " " + dict_int['lowercase'])
parallel_3 = {
    "uppercase": runnable1,
    "lowercase": runnable2
} | RunnableLambda(lambda dict_int: dict_int['uppercase'] + " " + dict_int['lowercase'])

result_3 = parallel_3.invoke("Ant Man")
print(result_3)

chain = (lambda input: str(input) + " Wow") | RunnableParallel({
     "uppercase": runnable1,
    "lowercase": runnable2
})

result_4 = chain.invoke("Chaowmow")
print(result_4)
