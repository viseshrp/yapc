#!/usr/bin/env python
from __future__ import annotations

import re
import sys

# Validation Rules
PROJECT_NAME_REGEX = r"^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9])\Z"
PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]*\Z"

project_name = "{{cookiecutter.project_name}}"
project_slug = "{{cookiecutter.project_slug}}"

# Validate project_name
if not re.match(PROJECT_NAME_REGEX, project_name):
    print(
        f"\033[91m[ERROR] '{project_name}' is not a valid CLI-friendly project name.\033[0m\n"
        "Use ASCII letters, numbers, periods, underscores, and hyphens; "
        "start and end with a letter or number."
    )
    sys.exit(1)

# Validate project_slug
if not re.match(PROJECT_SLUG_REGEX, project_slug):
    print(
        f"\033[91m[ERROR] '{project_slug}' is not a valid Python module name.\033[0m\n"
        "Use letters, numbers, and underscores, and do not start with a number."
    )
    sys.exit(1)
