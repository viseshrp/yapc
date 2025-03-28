{{cookiecutter.project_name}}
=============================

[![image](https://img.shields.io/pypi/v/{{cookiecutter.project_name}}.svg)](https://pypi.python.org/pypi/{{cookiecutter.project_name}})
[![Python versions](https://img.shields.io/pypi/pyversions/{{cookiecutter.project_name}}.svg?logo=python&logoColor=white)](https://pypi.org/project/{{cookiecutter.project_name}}/)
[![Tests status](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/workflows/Test/badge.svg)](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/actions?query=workflow%3ATest)
[![Coverage](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/branch/develop/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/blob/develop/LICENSE)
[![Downloads](https://pepy.tech/badge/{{cookiecutter.project_name}})](https://pepy.tech/project/{{cookiecutter.project_name}})

{{cookiecutter.project_description}}

![demo](https://raw.githubusercontent.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/develop/demo.gif)

Why build this
--------------


How it works
------------



Installation
------------

``` {.bash}
pip install {{cookiecutter.project_name}}
```

Requirements
------------

- Python 3.9+

Features
--------

- stuff

Usage
-----

<!-- [[[cog
import cog
from {{cookiecutter.project_name}} import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.main, ["--help"])
out = result.output.replace("Usage: main", "Usage: {{cookiecutter.project_name}}")
cog.out(
    "``` {{.bash}}\n"
    "$ {{cookiecutter.project_name}} --help\n"
    "```".format(out)
)
]]] -->
<!-- [[[end]]] -->

Limitations
-----------






Getting started with your project
---------------------------------

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

{% if cookiecutter.publish_to_pypi == "y" -%}

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/settings/secrets/actions/new).
- Create a [new release](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/cicd/#how-to-trigger-a-release).
{%- endif %}

---

Repository initiated with [{{cookiecutter.author_github_handle}}/yapc](https://github.com/{{cookiecutter.author_github_handle}}/yapc).



Credits
-------

- [Click](https://click.palletsprojects.com), for making writing CLI
    tools a complete pleasure.
- [Simon Willison](https://github.com/simonw/sqlite-utils/) for some
    inspiration.
