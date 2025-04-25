import pytest
from click.testing import CliRunner

from {{cookiecutter.project_slug}} import __version__, cli, exceptions


@pytest.mark.parametrize(
    "options",
    [
        ([]),
        (["-h"]),
        (["--help"]),
    ],
)
def test_help(options):
    result = CliRunner().invoke(cli.main, options)
    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")
    assert "-h, --help" in result.output


@pytest.mark.parametrize(
    "options",
    [
        (["-v"]),
        (["--version"]),
    ],
)
def test_version(options):
    result = CliRunner().invoke(cli.main, options)
    assert result.exit_code == 0
    assert __version__ in result.output
