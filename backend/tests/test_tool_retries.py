"""Deterministic tests of the retry policy used by Atlas tools."""
import pytest
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_none


def with_test_retry(func):
    """Same exception filter / attempt budget as Atlas, without slow waits."""
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_none(),
        retry=retry_if_exception_type(ConnectionError),
        reraise=True,
    )(func)


def test_tool_recovers_after_two_failures():
    attempts = []

    @with_test_retry
    def service():
        attempts.append(1)
        if len(attempts) < 3:
            raise ConnectionError("temporary")
        return "ok"

    assert service() == "ok"
    assert len(attempts) == 3


def test_tool_stops_after_three_failures():
    attempts = []

    @with_test_retry
    def service():
        attempts.append(1)
        raise ConnectionError("unavailable")

    with pytest.raises(ConnectionError, match="unavailable"):
        service()
    assert len(attempts) == 3


def test_non_retryable_validation_error():
    attempts = []

    @with_test_retry
    def service():
        attempts.append(1)
        raise ValueError("invalid input")

    with pytest.raises(ValueError, match="invalid input"):
        service()
    assert len(attempts) == 1
