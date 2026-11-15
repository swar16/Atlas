
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage



project_root = Path(__file__).resolve().parents[3]
load_dotenv(project_root / ".env")
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