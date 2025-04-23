"""Console script for {{cookiecutter.project_slug}}."""
import warnings

import click
from click_default_group import DefaultGroup

from . import __version__ as _version
from .{{cookiecutter.project_slug}} import do_stuff


warnings.filterwarnings("ignore")
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(
    cls=DefaultGroup,
    context_settings=CONTEXT_SETTINGS,
)
@click.version_option(_version, "-v", "--version")
def main():
    """
    {{cookiecutter.project_description}}

    \b
    Example usages:

    """
    pass


@main.command(default=True)
def subcommand(**kwargs):
    """
    Subcommand to do stuff.
    """
    click.echo("Doing stuff...")
    do_stuff(**kwargs)
    click.echo("Done!")


if __name__ == "__main__":
    main()
