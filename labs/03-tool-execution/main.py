import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
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
tool_registry = {
    "add": add,
    "multiply": multiply
}
model_with_tools=model.bind_tools(tools)
while(True):

    question = input("Ask a question (or 'quit' to exit): ")
    if question.lower() == "quit":
        break
    messages.append({"role": "user", "content": question})
    response = model_with_tools.invoke(messages)
    messages.append(response)
    if response.tool_calls:
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = tool_registry[tool_name]
            result = selected_tool.invoke(tool_args)
            messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )
        final_response = model_with_tools.invoke(messages)
        messages.append(final_response)
    else:
        final_response = response
    
    print("Content:", final_response.content)