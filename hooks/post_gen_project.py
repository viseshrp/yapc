#!/usr/bin/env python
from __future__ import annotations

import shutil
from pathlib import Path

PROJECT_DIRECTORY = Path.cwd().resolve()


def remove_file(path: str) -> None:
    full_path = PROJECT_DIRECTORY / path
    if full_path.is_file():
        full_path.unlink()


def remove_dir(path: str) -> None:
    full_path = PROJECT_DIRECTORY / path
    if full_path.is_dir():
        shutil.rmtree(full_path)


def move_file(src: str, dst: str) -> None:
    shutil.move(str(PROJECT_DIRECTORY / src), str(PROJECT_DIRECTORY / dst))


def move_dir(src: str, dst: str) -> None:
    shutil.move(str(PROJECT_DIRECTORY / src), str(PROJECT_DIRECTORY / dst))


if __name__ == "__main__":
    # GitHub Actions cleanup
    if "{{cookiecutter.include_github_actions}}" != "y":
        remove_dir(".github")
    elif "{{cookiecutter.publish_to_pypi}}" == "n":
        remove_file(".github/workflows/on-release-main.yml")

    # Codecov config
    if "{{cookiecutter.codecov}}" != "y":
        remove_file("codecov.yaml")
        if "{{cookiecutter.include_github_actions}}" == "y":
            remove_file(".github/workflows/validate-codecov-config.yml")

    if "{{cookiecutter.cli_tool}}" != "y":
        remove_file("{cookiecutter.project_slug}/__main__.py")
        remove_file("{cookiecutter.project_slug}/cli.py")
