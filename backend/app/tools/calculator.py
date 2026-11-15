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
def divide(a: int, b: int) -> float:
    """Divide two numbers where a and b are integers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers where a and b are integers."""
    return a - b
