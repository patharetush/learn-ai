from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-5.2",
    temperature=0
)

streamed_response = model.stream("Tell me about MCP server in agentic AI")

for chunk in streamed_response:
    print(chunk.content, end="", flush= True)