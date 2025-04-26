# {{cookiecutter.project_name}}

[![PyPI version](https://img.shields.io/pypi/v/{{cookiecutter.project_name}}.svg)](https://pypi.org/project/{{cookiecutter.project_name}})
[![Python versions](https://img.shields.io/pypi/pyversions/{{cookiecutter.project_name}}.svg?logo=python&logoColor=white)](https://pypi.org/project/{{cookiecutter.project_name}}/)
{% if cookiecutter.github_actions == 'y' %}
[![Test Status](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/workflows/Test/badge.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/actions?query=workflow%3ATest)
[![Coverage](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.project_name}})
{% endif %}
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/{{cookiecutter.project_name}})](https://pepy.tech/project/{{cookiecutter.project_name}})

> {{cookiecutter.project_description}}

![Demo](https://raw.githubusercontent.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/main/demo.gif)

---

## 🚀 Why this project exists

Explain the problem this tool solves or the goal it's intended to fulfill.

---

## 🧠 How this project works

Explain how the tool works.

---

## 🛠️ Features

* Does stuff

---

## 📦 Installation

```bash
pip install {{cookiecutter.project_name}}
```

---

## 🧪 Usage

{% if cookiecutter.cli_tool == 'y' %}
{% raw %}
<!-- [[[cog
import cog
from {{cookiecutter.project_slug}} import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.main, ["--help"])
out = result.output.replace("Usage: main", "Usage: {{cookiecutter.project_name}}")
result = runner.invoke(cli.what, ["--help"])
what_out = result.output
cog.out(
    "``` {{.bash}}\n"
    "$ {{cookiecutter.project_name}} --help\n"
    "{}"
    "```".format(out)
)
]]] -->
<!-- [[[end]]] -->
{% endraw %}
{% endif %}

---

## 📐 Requirements

- Python >= 3.9

---

## 🧾 Changelog

See [CHANGELOG.md](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}/blob/main/CHANGELOG.md)

---

## 🙏 Credits

{% if cookiecutter.cli_tool == "y" %}- [Click](https://click.palletsprojects.com), for enabling delightful CLI development. {% endif %}
- Inspired by [Simon Willison](https://github.com/simonw/sqlite-utils)

---

## 📄 License

MIT © [{{cookiecutter.author}}](https://github.com/{{cookiecutter.github_username}})
