import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from tools import add, get_secret_number, multiply

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
tools=[add, multiply, get_secret_number]
tool_registry = {
    "add": add,
    "multiply": multiply,
    "get_secret_number": get_secret_number
}
model_with_tools=model.bind_tools(tools)
MAX_TOOL_CALLS = 10
while(True):

    question = input("Ask a question (or 'quit' to exit): ")
    if question.lower() == "quit":
        break
    messages.append({"role": "user", "content": question})
    
    for step in range(MAX_TOOL_CALLS):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        print(f"Agent step: {step + 1}")
        if not response.tool_calls:
            print("Assistant:", response.content)
            break
     
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"Executing: {tool_name}({tool_args})")

            try:
                selected_tool = tool_registry[tool_name]
                result = selected_tool.invoke(tool_args)

            except Exception as e:
                result = f"Tool execution failed: {type(e).__name__}"
            messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )
    else:
        print("Agent reached maximum steps.")

    
    
    