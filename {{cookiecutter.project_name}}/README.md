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


Limitations
-----------


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
