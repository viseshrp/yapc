"""Console script for {{cookiecutter.project_slug}}."""
import click

from . import __version__ as _version
from .exceptions import CustomException
from .{{cookiecutter.project_slug}} import do_stuff


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(_version, "-v", "--version")
def main() -> None:
    """
    {{cookiecutter.project_description}}

    \b
    Example usages:

    """
    try:
        do_stuff()
    except CustomException as e:
        raise click.ClickException(str(e))
    except Exception as e:
        # all other exceptions
        raise click.ClickException(
            f"An unknown error occurred :: {e}\n"
        )


if __name__ == "__main__":
    main()  # pragma: no cover
