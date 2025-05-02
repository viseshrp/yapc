from datetime import datetime


def version_scheme(version):
    """Generate a version like 0.1.1.dev20250430173015"""
    base_version = version.tag.base_version if version.tag else "0.0.0"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # no 'T'
    return f"{base_version}.dev{timestamp}"


def local_scheme(version):
    """Disable local versioning (e.g., +gabcdef)"""
    return ""
