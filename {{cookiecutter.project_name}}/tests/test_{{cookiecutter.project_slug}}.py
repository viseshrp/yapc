import pytest


@pytest.mark.parametrize(
    "options",
    [
        "test1",
        "test2"
    ],
)
def test_do_stuff(options) -> None:
    print(options)
    assert True
