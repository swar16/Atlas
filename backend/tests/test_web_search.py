import pytest

from app.tools import web_search as web_search_module


def test_web_search_returns_sourced_results(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    class FakeTavilyClient:
        def __init__(self, api_key):
            assert api_key == "test-key"

        def search(self, **kwargs):
            assert kwargs == {
                "query": "latest Python release",
                "search_depth": "basic",
                "max_results": 5,
            }
            return {
                "query": "latest Python release",
                "results": [
                    {
                        "title": "Python News",
                        "url": "https://example.com/python",
                        "content": "Release details",
                        "score": 0.9,
                    }
                ],
            }

    monkeypatch.setattr(web_search_module, "TavilyClient", FakeTavilyClient)

    result = web_search_module.web_search.invoke({"query": " latest Python release "})

    assert result == {
        "query": "latest Python release",
        "results": [
            {
                "title": "Python News",
                "url": "https://example.com/python",
                "content": "Release details",
            }
        ],
    }


@pytest.mark.parametrize("query", ["", "   ", "x" * 401])
def test_web_search_rejects_invalid_queries(query):
    with pytest.raises(ValueError):
        web_search_module.web_search.invoke({"query": query})


def test_web_search_uses_keyless_api_when_no_key_is_configured(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"query": "current weather", "results": []}

    def fake_post(url, headers, json, timeout):
        assert url == "https://api.tavily.com/search"
        assert headers == {"X-Tavily-Access-Mode": "keyless"}
        assert json["query"] == "current weather"
        assert timeout == 15
        return FakeResponse()

    monkeypatch.setattr(web_search_module.requests, "post", fake_post)

    result = web_search_module.web_search.invoke({"query": "current weather"})

    assert result == {"query": "current weather", "results": []}
