from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.5",
    input="what is the weather in Paris?"
)

print("=" * 60)
print("response:")
print(response)
print("=" * 60)