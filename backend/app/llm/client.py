
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage



project_root = Path(__file__).resolve().parents[3]
load_dotenv(project_root / ".env")
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise RuntimeError(
        "API_KEY is not set."
    )
model = ChatOpenAI( 
    # model="openai/gpt-oss-20b",
    api_key=api_key,
    # base_url="https://integrate.api.nvidia.com/v1",
    model="north-mini-code-1.0",
    # base_url="https://openrouter.ai/api/v1",
    base_url="https://api.cohere.ai/compatibility/v1",
)