# {{cookiecutter.project_name}}

[![PyPI version](https://img.shields.io/pypi/v/{{cookiecutter.project_name}}.svg)](https://pypi.org/project/{{cookiecutter.project_name}}/)
[![Python versions](https://img.shields.io/pypi/pyversions/{{cookiecutter.project_name}}.svg?logo=python&logoColor=white)](https://pypi.org/project/{{cookiecutter.project_name}}/)
{% if cookiecutter.github_actions == 'y' -%}
[![CI](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/actions/workflows/main.yml/badge.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/actions/workflows/main.yml)
{%- endif %}
{% if cookiecutter.codecov == 'y' -%}
[![Coverage](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.project_name}})
{%- endif %}
[![License: MIT](https://img.shields.io/github/license/{{cookiecutter.github_username}}/{{cookiecutter.project_name}})](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/blob/main/LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![Lint: Ruff](https://img.shields.io/badge/lint-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![Typing: mypy](https://img.shields.io/badge/typing-checked-blue.svg)](https://mypy.readthedocs.io/en/stable/)

> {{cookiecutter.project_description}}

![Demo](https://raw.githubusercontent.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/main/demo.gif)

## 🚀 Why this project exists

Explain the problem this tool solves or the goal it's intended to fulfill.

## 🧠 How this project works

Explain how the tool works.

## 🛠️ Features

* Does stuff

## 📦 Installation

```bash
pip install {{cookiecutter.project_name}}
```

## 🧪 Usage
{% if cookiecutter.cli_tool == 'y' %}
* To view the help message, run the following command:

```bash
{{cookiecutter.project_name}} --help
```
{%- endif %}

## 📐 Requirements

* Python >= 3.9

## 🧾 Changelog

See [CHANGELOG.md](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/blob/main/CHANGELOG.md)

## 🙏 Credits

{% if cookiecutter.cli_tool == "y" -%}
* [Click](https://click.palletsprojects.com), for enabling delightful CLI development.
{% endif -%}
* Inspired by [Simon Willison](https://github.com/simonw)'s work.

## 📄 License

MIT © [{{cookiecutter.author}}](https://github.com/{{cookiecutter.github_username}})
