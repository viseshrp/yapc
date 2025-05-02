from __future__ import annotations

from datetime import datetime
from hatch_vcs.version import VCSVersion


def version_scheme(version: VCSVersion) -> str:
    """Generate a version like 0.1.1.dev20250430173015"""
    try:
        base_version = version.tag.base_version if version.tag else "0.0.0"
    except Exception:
        base_version = "0.0.0"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base_version}.dev{timestamp}"


def local_scheme(version: VCSVersion) -> str:
    """Disable local versioning (e.g., +gabcdef)"""
    return ""
