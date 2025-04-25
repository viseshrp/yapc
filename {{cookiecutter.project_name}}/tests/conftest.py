import pytest


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    print("cleanup")
