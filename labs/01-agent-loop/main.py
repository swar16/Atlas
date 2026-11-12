import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("OPENROUTER_KEY")
if not api_key:
    raise RuntimeError(
        "OPENROUTER_KEY is not set."
    )
model = ChatOpenAI(
    model="cohere/north-mini-code:free",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)
messages = []

while(True):
    question = input("Ask a question (or 'quit' to exit): ")
    if question.lower() == "quit":
        break
    messages.append({"role": "user", "content": question})
    response = model.invoke(messages)
    messages.append({"role": "assistant", "content": response.content})
    print(f"Assistant: {response.content}")
