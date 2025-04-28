import pytest

from {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}} import do_stuff


@pytest.mark.parametrize(
    "option",
    [
        "test1",
        "test2"
    ],
)
def test_do_stuff(option) -> None:
    assert do_stuff(option) == option
