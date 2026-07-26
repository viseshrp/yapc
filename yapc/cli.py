from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


import sys


def main() -> None:
    cwd = Path(__file__).parent
    package_dir = cwd.parent.resolve()

    if not (package_dir / "cookiecutter.json").exists():
        print(f"\033[91m[ERROR] Cookiecutter template files not found at: {package_dir}\033[0m", file=sys.stderr)
        sys.exit(1)

    cookiecutter_exe = shutil.which("cookiecutter") or "cookiecutter"

    try:
        subprocess.run(
            [cookiecutter_exe, str(package_dir)],
            check=True,
        )
    except FileNotFoundError:
        print("\033[91m[ERROR] 'cookiecutter' command was not found. Please install cookiecutter (e.g., `uv pip install cookiecutter`).\033[0m", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
