# Atlas

Atlas is a terminal-based AI agent built with LangGraph. It can answer questions, call tools, search the live web, and resume conversations after the application restarts. The project also includes small labs that show how the agent evolved from a basic loop into a graph-based tool-using agent.

## What it can do

- **Use tools across multiple steps.** The agent can combine tool calls with model responses and stops after a budget of 10 model steps.
- **Search the live web.** The Tavily-backed search tool returns up to five results with titles, URLs, and excerpts. Set `TAVILY_API_KEY` to use an authenticated Tavily account; when it is unset, the tool uses Tavily's rate-limited keyless mode.
- **Perform calculations.** Addition, subtraction, multiplication, and division are available as tools. Division by zero is rejected.
- **Persist conversations.** A PostgreSQL checkpointer stores graph state by conversation ID, so a conversation can be resumed in a later run.
- **Save user preferences.** Preferences entered with `:remember` are stored in PostgreSQL and supplied to the agent when relevant. Use `:preferences` to list them.
- **Retry transient model errors.** The graph retries model calls for connection errors, timeouts, and server errors, with a bounded exponential delay.

The project also has sample tools for a random number, age validation, and simulated unreliable services. These are useful for exploring tool calling, validation, and retry behavior.

## Requirements

- Python 3.10 or newer
- A PostgreSQL database reachable by the application
- A Cohere API key for the configured chat model
- Optional: a Tavily API key for authenticated web search

## Setup

From the project root, create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root. You can start with `.env.example`, then set the values for your environment:

```dotenv
COHERE_API_KEY=your-cohere-api-key
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require
ATLAS_USER_ID=default
# Optional. If omitted, Tavily's rate-limited keyless mode is used.
TAVILY_API_KEY=your-tavily-api-key
```

`COHERE_API_KEY` is read by the model client. The current model and Cohere-compatible endpoint are configured in `backend/app/llm/client.py`.

## Run Atlas

From the project root:

```bash
cd backend
python -m app.main
```

On first startup, Atlas initializes the PostgreSQL checkpoint and store tables. Enter a conversation ID to resume an existing conversation, or leave it blank to start a new one. Atlas prints the new ID; save it to resume that conversation later. Each `:new` command starts a separate conversation.

Available commands:

| Command | Action |
| --- | --- |
| `:remember <preference>` | Save a preference for the configured user |
| `:preferences` | List saved preferences |
| `:new` | Start a new conversation |
| `:quit` or `quit` | Exit Atlas |

Set `ATLAS_USER_ID` in `.env` to use a distinct preference namespace. The conversation ID selects the saved conversation; the user ID selects the saved preferences.

## Project layout

```text
backend/
  app/
    agent/       LangGraph state, nodes, routing, and retries
    llm/         Chat model configuration
    tools/       Calculator, sample tools, and web search
    main.py      Terminal interface and PostgreSQL setup
  tests/         Tests for agent limits, retries, and web search
labs/            Earlier agent and tool-calling experiments
```

## Tests

Run the backend test suite from the project root:

```bash
cd backend
python -m pytest
```

Some tests use mocked services; the suite does not require live model or Tavily calls.

## Notes

- Do not commit `.env` or put API keys in source control.
- Web search requires an internet connection. Keyless mode is subject to Tavily's rate limits.
- PostgreSQL must be reachable before starting the CLI.
- The graph retry policy applies to transient model API failures. Tool-specific behavior is implemented by each tool.
