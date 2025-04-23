from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import yaml


def is_valid_yaml(path: str | Path) -> bool:
    path = Path(path)

    if not path.is_file():
        print(f"File does not exist: {path}")
        return False

    try:
        with path.open("r", encoding="utf-8") as file:
            yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Invalid YAML file: {path} - Error: {e}")
        return False
    except OSError as e:
        print(f"Error reading file: {path} - Error: {e}")
        return False

    return True


@contextmanager
def run_within_dir(path: str | Path):
    path = Path(path).resolve()
    oldpwd = Path.cwd()
    try:
        # Switch directory
        os.chdir(path)
        yield
    finally:
        # Restore directory
        os.chdir(oldpwd)


def file_contains_text(file: str | Path, text: str) -> bool:
    file = Path(file)
    if not file.is_file():
        return False
    return text in file.read_text(encoding="utf-8")
