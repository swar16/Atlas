from langchain_core.tools import tool

from langchain_core.tools import tool
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging
@tool
def validate_age(age: int) -> str:
    """Validate a person's age. Age must be between 0 and 120."""
    if not 0 <= age <= 120:
        raise ValueError("Age must be between 0 and 120.")

    return f"Valid age: {age}"


@tool
def unreliable_service() -> str:
    """Simulate an external service that is temporarily unavailable."""
    raise ConnectionError("Service temporarily unavailable")



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

attempts = 0


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5),
    retry=retry_if_exception_type(ConnectionError),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def call_external_service():
    # global attempts
    # attempts += 1

    # print(f"Service attempt: {attempts}")

    # if attempts <= 2:
    #     raise ConnectionError("Temporary service failure")

    # return "Service responded successfully"

    print("Attempting external service...")
    raise ConnectionError("Service permanently unavailable")


@tool
def flaky_service() -> str:
    """Call a simulated external service that may temporarily fail."""
    return call_external_service()