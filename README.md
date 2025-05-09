
# yapc

[![Build status](https://img.shields.io/github/actions/workflow/status/viseshrp/yapc/main.yml?branch=main)](https://github.com/viseshrp/yapc/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/viseshrp/yapc/blob/main/pyproject.toml)
[![License](https://img.shields.io/github/license/viseshrp/yapc)](https://img.shields.io/github/license/viseshrp/yapc)

This is a modern Cookiecutter template that can be used to initiate a Python project with
all the necessary tools for development, testing, and deployment. It supports the following features:

## Features

- 🧹 **Dependency management** with [uv](https://docs.astral.sh/uv/)
- 🛠️ **Automated code formatting** with [black](https://black.readthedocs.io/en/stable/) and [ruff-format](https://docs.astral.sh/ruff/formatter/)
- 🔍 **Linting** with [ruff](https://docs.astral.sh/ruff/) (enforces pyflakes, pycodestyle, pyupgrade, isort, tryceratops, and more)
- 🧠 **Static type checking** with [mypy](https://mypy.readthedocs.io/en/stable/)
- 🚨 **Security scanning** with [bandit](https://bandit.readthedocs.io/en/latest/) and [safety](https://pyup.io/safety/)
- 🧹 **Dead code detection** with [vulture](https://github.com/jendrikseipp/vulture)
- 📦 **Dependency health checking** with [deptry](https://github.com/fpgmaas/deptry)
- 📄 **Typo checking** with [codespell](https://github.com/codespell-project/codespell)
- 📝 **Markdown linting** with [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli)
- 🧪 **Testing** with [pytest](https://docs.pytest.org/en/stable/) and [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
- 🛡️ **Test coverage reporting** with [Codecov](https://about.codecov.io/) (optional)
- 🏗️ **Multi-version Python testing** with [tox-uv](https://github.com/tox-dev/tox-uv) and GitHub Actions matrix (3.9–3.13)
- 🛠️ **Pre-commit hook management** with [pre-commit](https://pre-commit.com/)
- 📦 **Optional CLI scaffolding** with [Click](https://click.palletsprojects.com/)
- 📦 **Optional PyPI publishing** setup (using uv)
- 🛠️ **CI-ready** with GitHub Actions workflows baked in

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/viseshrp/yapc.git
```

or if you don't have `uv` installed yet:

```bash
pip install cookiecutter
cookiecutter https://github.com/viseshrp/yapc.git
```

Follow the prompts to configure your project. Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

## Acknowledgements

This project is based on the [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) repository.
