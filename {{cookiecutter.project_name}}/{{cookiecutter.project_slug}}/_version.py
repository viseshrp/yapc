from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("{{ cookiecutter.project_name }}")
except PackageNotFoundError:  # pragma: no cover
    # Fallback for local dev or editable installs
    __version__ = "0.0.0"
