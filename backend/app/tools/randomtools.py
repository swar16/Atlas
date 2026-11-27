
from langchain_core.tools import tool
import random

@tool 
def get_secret_number()->int:
    """Get a secret number between 1 and 100."""
    return random.randint(1, 100)