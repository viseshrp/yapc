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
    # Codecov config
    if "{{ cookiecutter.codecov }}" != "y":
        remove_file("codecov.yml")
        remove_file(".github/workflows/validate-codecov-config.yml")

    if "{{ cookiecutter.cli_tool }}" != "y":
        remove_file("{{ cookiecutter.project_slug }}/__main__.py")
        remove_file("{{ cookiecutter.project_slug }}/cli.py")
        remove_file("tests/test_cli.py")

    if "{{ cookiecutter.github_actions }}" != "y":
        remove_dir(".github/actions")
        remove_dir(".github/workflows")

    if "{{ cookiecutter.git_init }}" == "y":
        git_exe = shutil.which("git")
        if git_exe:
            subprocess.run(
                [git_exe, "init", "-b", "main"],
                cwd=PROJECT_DIRECTORY,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            subprocess.run(
                [git_exe, "config", "user.name", "{{ cookiecutter.author }}"],
                cwd=PROJECT_DIRECTORY,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            subprocess.run(
                [git_exe, "config", "user.email", "{{ cookiecutter.email }}"],
                cwd=PROJECT_DIRECTORY,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            subprocess.run(
                [git_exe, "add", "."],
                cwd=PROJECT_DIRECTORY,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            subprocess.run(
                [git_exe, "commit", "-m", "Init commit", "--no-verify"],
                cwd=PROJECT_DIRECTORY,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            subprocess.run(
                [
                    git_exe,
                    "remote",
                    "add",
                    "origin",
                    "git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}.git",
                ],
                cwd=PROJECT_DIRECTORY,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
