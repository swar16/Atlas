from langgraph.graph import END, START, StateGraph

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
graph.add_node("agent_node", agent_node)
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
