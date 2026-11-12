import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools import add, multiply

load_dotenv("../../.env")

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
tools=[add, multiply]
model_with_tools=model.bind_tools(tools)
while(True):
    question = input("Ask a question (or 'quit' to exit): ")
    if question.lower() == "quit":
        break
    messages.append({"role": "user", "content": question})
    response = model_with_tools.invoke(messages)
    messages.append({"role": "assistant", "content": response.content})
    print("Content:", response.content)
    print("Tool Calls:", response.tool_calls)

