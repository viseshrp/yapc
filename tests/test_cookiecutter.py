from __future__ import annotations

import shutil
import subprocess

from tests.utils import file_contains_text, is_valid_yaml, run_within_dir


def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "my-project"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "my-project"
    assert result.project_path.is_dir()


def test_using_pytest(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.name == "example-project"
        assert result.project_path.is_dir()
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")

        with run_within_dir(result.project_path):
            uv_exe = shutil.which("uv") or "uv"
            subprocess.run([uv_exe, "sync"], check=True)
            subprocess.run([uv_exe, "run", "make", "test"], check=True)


def test_cicd_contains_pypi_secrets(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"publish_to_pypi": "y"})

        assert result.exit_code == 0
        workflow = result.project_path / ".github" / "workflows" / "on-release-main.yml"
        makefile = result.project_path / "Makefile"
        assert is_valid_yaml(workflow)
        assert file_contains_text(workflow, "PYPI_TOKEN")
        assert file_contains_text(makefile, "build-and-publish")


def test_tox(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()

        tox_file = result.project_path / "tox.ini"
        assert result.exit_code == 0
        assert tox_file.is_file()
        assert file_contains_text(tox_file, "[tox]")


def test_codecov(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()

        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert (result.project_path / "codecov.yaml").is_file()
        assert (result.project_path / ".github" / "workflows" / "validate-codecov-config.yml").is_file()


def test_not_codecov(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"codecov": "n"})

        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert not (result.project_path / "codecov.yaml").is_file()
        assert not (result.project_path / ".github" / "workflows" / "validate-codecov-config.yml").is_file()


def test_remove_release_workflow(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"publish_to_pypi": "n"})

        assert result.exit_code == 0
        assert not (result.project_path / ".github" / "workflows" / "on-release-main.yml").is_file()


def test_license_mit(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()

        license_path = result.project_path / "LICENSE"
        assert result.exit_code == 0
        assert license_path.is_file()

        with license_path.open(encoding="utf-8") as licfile:
            lines = licfile.readlines()
            assert len(lines) == 21
