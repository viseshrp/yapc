import pytest


@pytest.fixture()
def cleanup():
    yield
    print("cleanup")