#!/usr/bin/env python
from __future__ import annotations

import shutil
import subprocess
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
    if "{{ cookiecutter.publish_to_pypi }}" == "n":
        remove_file(".github/workflows/release.yml")

    # Codecov config
    if "{{ cookiecutter.codecov }}" != "y":
        remove_file("codecov.yaml")
        remove_file(".github/workflows/validate-codecov-config.yml")

    if "{{ cookiecutter.cli_tool }}" != "y":
        remove_file("{{ cookiecutter.project_slug }}/__main__.py")
        remove_file("{{ cookiecutter.project_slug }}/cli.py")
        remove_file("tests/test_cli.py")

    if "{{ cookiecutter.github_actions }}" != "y":
        remove_dir(".github/actions")
        remove_dir(".github/workflows")

    # If Git is available, initialize a repo with a tag for hatch-vcs
    git_exe = shutil.which("git")
    if git_exe:
        subprocess.run([git_exe, "init"], cwd=PROJECT_DIRECTORY, check=True)
        subprocess.run([git_exe, "add", "."], cwd=PROJECT_DIRECTORY, check=True)
        subprocess.run([git_exe, "commit", "-m", "Initial commit"], cwd=PROJECT_DIRECTORY, check=True)
        subprocess.run([git_exe, "tag", "v0.0.1"], cwd=PROJECT_DIRECTORY, check=True)
