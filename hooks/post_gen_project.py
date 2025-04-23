#!/usr/bin/env python
from __future__ import annotations

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(path: str) -> None:
    full_path = os.path.join(PROJECT_DIRECTORY, path)
    if os.path.isfile(full_path):
        os.remove(full_path)


def remove_dir(path: str) -> None:
    full_path = os.path.join(PROJECT_DIRECTORY, path)
    if os.path.isdir(full_path):
        shutil.rmtree(full_path)


def move_file(src: str, dst: str) -> None:
    shutil.move(os.path.join(PROJECT_DIRECTORY, src), os.path.join(PROJECT_DIRECTORY, dst))


def move_dir(src: str, dst: str) -> None:
    shutil.move(os.path.join(PROJECT_DIRECTORY, src), os.path.join(PROJECT_DIRECTORY, dst))


if __name__ == "__main__":
    # GitHub Actions cleanup
    if "{{cookiecutter.include_github_actions}}" != "y":
        remove_dir(".github")
    elif "{{cookiecutter.publish_to_pypi}}" == "n":
        remove_file(".github/workflows/on-release-main.yml")

    # Dockerfile
    if "{{cookiecutter.dockerfile}}" != "y":
        remove_file("Dockerfile")

    # Codecov config
    if "{{cookiecutter.codecov}}" != "y":
        remove_file("codecov.yaml")
        if "{{cookiecutter.include_github_actions}}" == "y":
            remove_file(".github/workflows/validate-codecov-config.yml")
