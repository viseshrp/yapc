from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from tests.utils import file_contains_text, is_valid_yaml, run_within_dir


def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "my-project"})

    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path is not None
    project_path = Path(result.project_path)
    assert project_path.name == "my-project"
    assert project_path.is_dir()


@pytest.mark.parametrize("cli_opt", ["y", "n"])
def test_using_pytest(cookies, tmp_path, cli_opt):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"cli_tool": cli_opt})
        project_path = Path(result.project_path)
        slug = project_path.name.replace("-", "_")
        (project_path / slug / "_version.py").write_text('__version__ = "0.0.0"\n')

        assert result.exit_code == 0
        assert result.exception is None
        assert project_path.name == "example-project"
        assert project_path.is_dir()
        assert is_valid_yaml(project_path / ".github" / "workflows" / "main.yml")

        with run_within_dir(project_path):
            uv_exe = shutil.which("uv") or "uv"
            make_exe = shutil.which("make") or "make"
            subprocess.run([uv_exe, "sync"], check=True)
            subprocess.run([make_exe, "test"], check=True)


def test_cicd_contains_pypi_secrets(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"publish_to_pypi": "y"})
        project_path = Path(result.project_path)

        workflow = project_path / ".github" / "workflows" / "release.yml"
        makefile = project_path / "Makefile"
        assert result.exit_code == 0
        assert is_valid_yaml(workflow)
        assert file_contains_text(workflow, "PYPI_TOKEN")
        assert file_contains_text(makefile, "build-and-publish")


def test_codecov(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()
        project_path = Path(result.project_path)

        assert result.exit_code == 0
        assert is_valid_yaml(project_path / ".github" / "workflows" / "main.yml")
        assert (project_path / "codecov.yml").is_file()
        assert (project_path / ".github" / "workflows" / "validate-codecov-config.yml").is_file()


def test_not_codecov(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"codecov": "n"})
        project_path = Path(result.project_path)

        assert result.exit_code == 0
        assert is_valid_yaml(project_path / ".github" / "workflows" / "main.yml")
        assert not (project_path / "codecov.yml").is_file()
        assert not (project_path / ".github" / "workflows" / "validate-codecov-config.yml").is_file()


def test_not_cli_tool(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"cli_tool": "n"})
        project_path = Path(result.project_path)

        assert result.exit_code == 0
        assert result.exception is None
        assert not (project_path / "example_project" / "__main__.py").is_file()
        assert not (project_path / "example_project" / "cli.py").is_file()
        assert not (project_path / "tests" / "test_cli.py").is_file()


def test_not_github_actions(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"github_actions": "n"})
        project_path = Path(result.project_path)

        assert result.exit_code == 0
        assert not (project_path / ".github" / "actions").is_dir()
        assert not (project_path / ".github" / "workflows").is_dir()


def test_remove_release_workflow(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"publish_to_pypi": "n"})
        project_path = Path(result.project_path)

        assert result.exit_code == 0
        assert not (project_path / ".github" / "workflows" / "release.yml").is_file()


def test_license_mit(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()
        project_path = Path(result.project_path)

        license_path = project_path / "LICENSE"
        assert result.exit_code == 0
        assert license_path.is_file()

        with license_path.open(encoding="utf-8") as licfile:
            lines = licfile.readlines()
            assert len(lines) == 21
