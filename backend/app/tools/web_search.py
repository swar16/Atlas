import os
import requests

from langchain_core.tools import tool
from tavily import TavilyClient


@tool
def web_search(query: str) -> dict:
    """Search the live web for current information and return sourced results."""
    query = query.strip()
    if not query:
        raise ValueError("Search query cannot be empty.")
    if len(query) > 400:
        raise ValueError("Search query must be 400 characters or fewer.")

    api_key = os.getenv("TAVILY_API_KEY")
    if api_key:
        response = TavilyClient(api_key=api_key).search(
            query=query,
            search_depth="basic",
            max_results=5,
        )
    else:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"X-Tavily-Access-Mode": "keyless"},
            json={
                "query": query,
                "search_depth": "basic",
                "max_results": 5,
            },
            timeout=15,
        )
        response.raise_for_status()
        response = response.json()
    return {
        "query": response.get("query", query),
        "results": [
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
            }
            for result in response.get("results", [])
        ],
    }
