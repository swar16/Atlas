from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
from typing import TypedDict


class TestState(TypedDict):
    result: str


attempts = 0


def failing_agent(state: TestState):
    global attempts
    attempts += 1

    print(f"Agent attempt: {attempts}")

    if attempts < 3:
        raise ConnectionError("Simulated model API failure")

    return {"result": "Model responded successfully"}


builder = StateGraph(TestState)

builder.add_node(
    "agent",
    failing_agent,
    retry_policy=RetryPolicy(
        max_attempts=3,
        initial_interval=0.1,
        retry_on=lambda error: isinstance(error, ConnectionError),
    ),
)

builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()

result = graph.invoke({"result": ""})

assert attempts == 3
assert result["result"] == "Model responded successfully"

print("Model retry test passed!")