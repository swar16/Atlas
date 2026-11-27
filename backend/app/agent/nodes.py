from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from app.agent.state import AgentState
from app.llm.client import model
from app.tools.calculator import add, multiply, subtract, divide
from app.tools.randomtools import get_secret_number
from app.tools.failing_tools import flaky_service, validate_age, unreliable_service

MAX_AGENT_STEPS = 2

tools = [add, multiply, subtract, divide,get_secret_number, validate_age, unreliable_service, flaky_service]
tool_node = ToolNode(tools)
model_with_tools = model.bind_tools(tools)


def agent_node(state: AgentState) -> dict:
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {
        "messages": [response],
        "agent_steps": state.get("agent_steps", 0) + 1,
    }


def route_after_agent(state: AgentState) -> str:
    messages = state["messages"]

    if messages[-1].tool_calls:
        return "tool_node"
    return "finished"


def route_after_tools(state: AgentState) -> str:
    if state["agent_steps"] >= MAX_AGENT_STEPS:
        return "limit_reached"
    return "agent_node"


def step_limit_node(state: AgentState) -> dict:
    return {
        "messages": [
            AIMessage(
                content=(
                    f"I reached the {MAX_AGENT_STEPS}-step tool-use limit before "
                    "finishing. You can ask me to continue or simplify the request."
                )
            )
        ]
    }
