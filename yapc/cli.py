from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def main() -> None:
    cwd = Path(__file__).parent
    package_dir = cwd.parent.resolve()

    cookiecutter_exe = shutil.which("cookiecutter") or "cookiecutter"

    subprocess.run(
        [cookiecutter_exe, str(package_dir)],
        check=True,
    )
