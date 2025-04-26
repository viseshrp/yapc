import pytest


@pytest.fixture(scope="session", autouse=True)
def cleanup() -> None:
    yield
    print("cleanup")
