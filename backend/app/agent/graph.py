from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy
from openai import (
    APITimeoutError,
    APIConnectionError,
    InternalServerError,
    RateLimitError,
)
def should_retry(error: Exception) -> bool:
    return isinstance(
        error,
        (
            APITimeoutError,
            APIConnectionError,
            InternalServerError,
        )
    )
from app.agent.nodes import (
    agent_node,
    route_after_agent,
    route_after_tools,
    step_limit_node,
    tool_node,
)
from app.agent.state import AgentState

graph = StateGraph(AgentState)
graph.add_node("tool_node", tool_node)
graph.add_node("agent_node", agent_node,retry_policy=RetryPolicy(
        max_attempts=3,
        initial_interval=1.0,
        backoff_factor=2.0,
        max_interval=10.0,
        jitter=True,
        retry_on=should_retry,
    ),)
graph.add_node("limit_reached", step_limit_node)
graph.add_edge(START, "agent_node")
graph.add_conditional_edges(
    "agent_node",
    route_after_agent,
    {
        "tool_node": "tool_node",
        "finished": END,
    },
)
graph.add_conditional_edges(
    "tool_node",
    route_after_tools,
    {
        "agent_node": "agent_node",
        "limit_reached": "limit_reached",
    },
)
graph.add_edge("limit_reached", END)

chatbot = graph.compile()
