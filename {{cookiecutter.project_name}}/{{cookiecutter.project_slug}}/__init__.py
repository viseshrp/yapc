{{ ("Top-level package for " ~ cookiecutter.project_name ~ ".")|tojson }}

from ._version import __version__
{% if cookiecutter.cli_tool == "y" -%}
from .cli import main
{%- endif %}

__all__ = ["__version__"{% if cookiecutter.cli_tool == "y" %}, "main"{% endif %}]
