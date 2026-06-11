from langchain_openai import ChatOpenAI
import asyncio

model = ChatOpenAI(
    model="gpt-5.2",
    temperature=0
)

async def stream_response_events():
    event_limit = 0
    prompt = "Describe the NBA"

    async for event_chunk in model.astream_events(prompt, version="v2"):
        event_limit += 1

        if event_limit >= 5:
            print("...event streaming done....")
            return

        print(event_chunk)

asyncio.run(stream_response_events())