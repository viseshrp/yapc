#!/usr/bin/env python
from __future__ import annotations

import json
import re
import sys
from email.headerregistry import Address

# Validation Rules
PROJECT_NAME_REGEX = r"^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9])\Z"
PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]*\Z"
GITHUB_USERNAME_REGEX = r"^(?!-)(?!.*--)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?\Z"

# fmt: off
project_name = json.loads(r'''{{ cookiecutter.project_name|tojson }}''')
project_slug = json.loads(r'''{{ cookiecutter.project_slug|tojson }}''')
author = json.loads(r'''{{ cookiecutter.author|tojson }}''')
email = json.loads(r'''{{ cookiecutter.email|tojson }}''')
github_username = json.loads(r'''{{ cookiecutter.github_username|tojson }}''')
project_description = json.loads(r'''{{ cookiecutter.project_description|tojson }}''')
# fmt: on

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

if not re.match(GITHUB_USERNAME_REGEX, github_username):
    print(
        f"\033[91m[ERROR] '{github_username}' is not a valid GitHub username.\033[0m\n"
        "Use 1-39 ASCII letters, numbers, or single hyphens; do not start or end with a hyphen."
    )
    sys.exit(1)

if not author or "," in author or "\r" in author or "\n" in author:
    print("\033[91m[ERROR] The author must be a non-empty email display name without commas or newlines.\033[0m")
    sys.exit(1)

try:
    Address(display_name=author, username="author", domain="example.invalid")
except ValueError:
    print("\033[91m[ERROR] The author is not a valid email display name.\033[0m")
    sys.exit(1)

try:
    Address(addr_spec=email)
except ValueError:
    print(f"\033[91m[ERROR] '{email}' is not a valid email address.\033[0m")
    sys.exit(1)

if "\r" in project_description or "\n" in project_description:
    print("\033[91m[ERROR] The project description must fit on one line.\033[0m")
    sys.exit(1)
