from langchain_core.tools import tool
import numpy as np
@tool
def add(a: int, b: int) -> int:
    """Add two numbers a and b where a and b are integers."""

    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers where a and b are integers."""
    return a * b

@tool
def get_secret_number() -> int:
    """Return a secret number unknown to the model."""
    return np.random.randint(1, 100)

