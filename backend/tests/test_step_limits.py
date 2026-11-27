"""Exercise Atlas's real routing and limit-message logic, without API calls.

These tests assume the existing backend/app/agent/nodes.py functions shown in Atlas:
route_after_tools(), step_limit_node(), and MAX_AGENT_STEPS.
"""
import pytest


@pytest.fixture
def nodes_module():
    # Imports initialize the model client but do NOT invoke the provider.
    # Requires your normal Atlas .env for COHERE_API_KEY.
    from app.agent import nodes
    return nodes


def test_routes_back_to_agent_below_limit(nodes_module, monkeypatch):
    monkeypatch.setattr(nodes_module, "MAX_AGENT_STEPS", 2)
    assert nodes_module.route_after_tools({"agent_steps": 1}) == "agent_node"


def test_routes_to_limit_at_budget(nodes_module, monkeypatch):
    monkeypatch.setattr(nodes_module, "MAX_AGENT_STEPS", 2)
    assert nodes_module.route_after_tools({"agent_steps": 2}) == "limit_reached"


def test_limit_node_gives_readable_message(nodes_module, monkeypatch):
    monkeypatch.setattr(nodes_module, "MAX_AGENT_STEPS", 2)
    result = nodes_module.step_limit_node({"messages": [], "agent_steps": 2})
    assert len(result["messages"]) == 1
    assert "2-step" in result["messages"][0].content
