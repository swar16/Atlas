"""Test LangGraph node retries with no real model/API calls."""
from typing import TypedDict

import pytest
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy


class State(TypedDict):
    result: str


class SimulatedProviderTimeout(Exception):
    pass


def build_graph(node):
    builder = StateGraph(State)
    builder.add_node(
        "agent_node",
        node,
        retry_policy=RetryPolicy(
            max_attempts=3,
            initial_interval=0.01,
            max_interval=0.02,
            jitter=False,
            retry_on=lambda e: isinstance(e, SimulatedProviderTimeout),
        ),
    )
    builder.add_edge(START, "agent_node")
    builder.add_edge("agent_node", END)
    return builder.compile()


def test_model_node_recovers_on_third_attempt():
    attempts = []

    def fake_agent(state):
        attempts.append(1)
        if len(attempts) < 3:
            raise SimulatedProviderTimeout("provider timed out")
        return {"result": "hello"}

    graph = build_graph(fake_agent)
    assert graph.invoke({"result": ""})["result"] == "hello"
    assert len(attempts) == 3


def test_model_node_exhausts_retry_budget():
    attempts = []

    def fake_agent(state):
        attempts.append(1)
        raise SimulatedProviderTimeout("provider down")

    graph = build_graph(fake_agent)
    with pytest.raises(SimulatedProviderTimeout, match="provider down"):
        graph.invoke({"result": ""})
    assert len(attempts) == 3


def test_model_node_does_not_retry_non_transient_failure():
    attempts = []

    def fake_agent(state):
        attempts.append(1)
        raise ValueError("bad configuration")

    graph = build_graph(fake_agent)
    with pytest.raises(ValueError, match="bad configuration"):
        graph.invoke({"result": ""})
    assert len(attempts) == 1
