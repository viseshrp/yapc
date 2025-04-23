from __future__ import annotations

from pathlib import Path
import subprocess


def main() -> None:
    cwd = Path(__file__).parent
    package_dir = cwd.parent.resolve()

    subprocess.run(
        ["cookiecutter", str(package_dir)],
        check=True,
    )
