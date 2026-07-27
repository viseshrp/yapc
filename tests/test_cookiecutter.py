from __future__ import annotations

import ast
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import tomli

from hooks import post_gen_project
from tests.utils import is_valid_yaml, run_within_dir


def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "my-project", "github_username": "project-owner"})

    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path is not None
    project_path = Path(result.project_path)
    assert project_path.name == "my-project"
    assert project_path.is_dir()
    automerge = (project_path / ".github" / "workflows" / "automerge.yml").read_text(encoding="utf-8")
    assert "'project-owner'" in automerge
    assert "'viseshrp'" not in automerge


@pytest.mark.parametrize(
    ("project_name", "project_slug"),
    [
        ("a", "a"),
        ("friendly.bard", "friendly_bard"),
        ("friendly_bard", "friendly_bard"),
        ("1-project", "_1_project"),
    ],
)
def test_valid_distribution_names_generate_importable_slugs(cookies, project_name, project_slug):
    result = cookies.bake(extra_context={"project_name": project_name})

    assert result.exit_code == 0, result.exception
    assert (Path(result.project_path) / project_slug / "__init__.py").is_file()


@pytest.mark.parametrize("project_name", ["-foo", "foo-", ".foo", "foo."])
def test_distribution_names_must_start_and_end_with_alphanumeric(cookies, project_name):
    result = cookies.bake(extra_context={"project_name": project_name})

    assert result.exit_code != 0


def test_user_text_is_safely_serialized_for_python_toml_and_yaml(cookies):
    author = 'Renée "Ada" O\'Connor'
    description = 'Handles "quotes", C:\\tmp, Unicode Ω, and delimiters """ plus \'\'\'.'
    result = cookies.bake(
        extra_context={
            "author": author,
            "email": "ada+test@example.com",
            "github_username": "octo-cat",
            "project_description": description,
            "git_init": "n",
        }
    )
    project_path = Path(result.project_path)

    assert result.exit_code == 0, result.exception

    pyproject = tomli.loads((project_path / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["description"] == description
    assert pyproject["project"]["authors"] == [{"name": author, "email": "ada+test@example.com"}]
    assert pyproject["project"]["scripts"]["example-project"] == "example_project.__main__:main"

    for python_path in project_path.rglob("*.py"):
        ast.parse(python_path.read_text(encoding="utf-8"), filename=str(python_path))

    cli_module = ast.parse((project_path / "example_project" / "cli.py").read_text(encoding="utf-8"))
    cli_function = next(node for node in cli_module.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    cli_docstring = ast.get_docstring(cli_function, clean=False)
    assert cli_docstring is not None
    assert cli_docstring.startswith(description)
    assert is_valid_yaml(project_path / ".github" / "workflows" / "automerge.yml")


@pytest.mark.parametrize(
    "extra_context",
    [
        {"github_username": "bad'name"},
        {"github_username": "bad\nname"},
        {"email": "not-an-email"},
        {"email": "ada@example.com\nBcc: other@example.com"},
        {"author": "Lovelace, Ada"},
        {"project_description": "first line\nsecond line"},
    ],
)
def test_invalid_metadata_values_are_rejected(cookies, extra_context):
    result = cookies.bake(extra_context=extra_context)

    assert result.exit_code != 0


def test_not_git_init_has_a_lockable_project(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"git_init": "n"})
        project_path = Path(result.project_path)

        assert result.exit_code == 0, result.exception
        assert not (project_path / ".git").exists()

        uv_exe = shutil.which("uv") or "uv"
        subprocess.run([uv_exe, "lock"], cwd=project_path, check=True)

        assert (project_path / "uv.lock").is_file()


def test_git_init_starts_an_uncommitted_repository(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(
            extra_context={
                "git_init": "y",
                "github_username": "project-owner",
                "project_name": "my-project",
            }
        )
        project_path = Path(result.project_path)

        assert result.exit_code == 0, result.exception
        assert (project_path / ".git").is_dir()
        assert not (project_path / "uv.lock").exists()

        git_exe = shutil.which("git")
        assert git_exe is not None

        branch = subprocess.run(
            [git_exe, "symbolic-ref", "--short", "HEAD"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert branch.stdout.strip() == "main"

        head = subprocess.run(
            [git_exe, "rev-parse", "--verify", "HEAD"],
            cwd=project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert head.returncode != 0

        status = subprocess.run(
            [git_exe, "status", "--short"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert "README.md" in status.stdout

        remote = subprocess.run(
            [git_exe, "remote", "get-url", "origin"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert remote.stdout.strip() == "git@github.com:project-owner/my-project.git"

        local_user = subprocess.run(
            [git_exe, "config", "--local", "--get", "user.name"],
            cwd=project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert local_user.returncode != 0


def test_git_init_requires_available_git(monkeypatch):
    monkeypatch.setattr(post_gen_project.shutil, "which", lambda _: None)

    with pytest.raises(SystemExit, match="Git initialization was requested"):
        post_gen_project.initialize_git()


def test_tagless_first_commit_has_development_version(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()
        project_path = Path(result.project_path)

        assert result.exit_code == 0, result.exception

        uv_exe = shutil.which("uv") or "uv"
        subprocess.run([uv_exe, "sync"], cwd=project_path, check=True)

        git_exe = shutil.which("git")
        assert git_exe is not None
        subprocess.run([git_exe, "add", "."], cwd=project_path, check=True)
        subprocess.run(
            [
                git_exe,
                "-c",
                "user.name=Template Test",
                "-c",
                "user.email=template-test@example.invalid",
                "commit",
                "-m",
                "Initial commit",
            ],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )

        tags = subprocess.run(
            [git_exe, "tag", "--list"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert tags.stdout == ""

        workflow = (project_path / ".github" / "workflows" / "main.yml").read_text(encoding="utf-8")
        assert "run: make check-dev-version" in workflow

        make_exe = shutil.which("make") or "make"
        version_check = subprocess.run(
            [make_exe, "check-dev-version"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert ".dev" in version_check.stdout


def test_release_helper_checks_state_before_pushing_tag(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()
        project_path = Path(result.project_path)
        remote_path = tmp_path / "remote.git"

        assert result.exit_code == 0, result.exception

        uv_exe = shutil.which("uv") or "uv"
        git_exe = shutil.which("git")
        bash_exe = shutil.which("bash")
        assert git_exe is not None
        assert bash_exe is not None

        subprocess.run([uv_exe, "sync"], cwd=project_path, check=True)
        subprocess.run([git_exe, "init", "--bare", str(remote_path)], check=True, capture_output=True, text=True)
        subprocess.run([git_exe, "remote", "set-url", "origin", str(remote_path)], cwd=project_path, check=True)
        subprocess.run([git_exe, "config", "user.name", "Template Test"], cwd=project_path, check=True)
        subprocess.run(
            [git_exe, "config", "user.email", "template-test@example.invalid"],
            cwd=project_path,
            check=True,
        )
        subprocess.run([git_exe, "add", "."], cwd=project_path, check=True)
        subprocess.run(
            [
                git_exe,
                "-c",
                "user.name=Template Test",
                "-c",
                "user.email=template-test@example.invalid",
                "commit",
                "-m",
                "Initial commit",
            ],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )

        development_version = subprocess.run(
            [uv_exe, "run", "hatch", "version"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        release_version = development_version.partition(".dev")[0]
        changelog_path = project_path / "CHANGELOG.md"
        changelog = changelog_path.read_text(encoding="utf-8")
        changelog_path.write_text(
            changelog.replace(
                "## [0.0.2] - <Unreleased>",
                f"## [{release_version}] - {date.today().isoformat()}",
            ),
            encoding="utf-8",
        )
        subprocess.run([git_exe, "add", "CHANGELOG.md"], cwd=project_path, check=True)
        subprocess.run(
            [
                git_exe,
                "-c",
                "user.name=Template Test",
                "-c",
                "user.email=template-test@example.invalid",
                "commit",
                "-m",
                "Prepare release",
            ],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run([git_exe, "push", "--set-upstream", "origin", "main"], cwd=project_path, check=True)

        untracked_path = project_path / "untracked.txt"
        untracked_path.write_text("not ready\n", encoding="utf-8")
        dirty = subprocess.run(
            [bash_exe, "scripts/tag_release.sh"],
            cwd=project_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert dirty.returncode != 0
        assert "tracked and untracked changes" in dirty.stderr
        untracked_path.unlink()

        released = subprocess.run(
            [bash_exe, "scripts/tag_release.sh"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        expected_tag = f"v{release_version}"
        assert f"Tag {expected_tag} pushed successfully" in released.stdout

        local_tags = subprocess.run(
            [git_exe, "tag", "--list", expected_tag],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert local_tags.stdout.strip() == expected_tag

        remote_tags = subprocess.run(
            [git_exe, "show-ref", "--verify", f"refs/tags/{expected_tag}"],
            cwd=remote_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert remote_tags.stdout.strip().endswith(f"refs/tags/{expected_tag}")


def test_release_workflows_publish_tested_tag_artifacts(cookies):
    result = cookies.bake()
    project_path = Path(result.project_path)

    assert result.exit_code == 0, result.exception

    workflows = project_path / ".github" / "workflows"
    main_workflow = (workflows / "main.yml").read_text(encoding="utf-8")
    release_workflow = (workflows / "release.yml").read_text(encoding="utf-8")

    assert not (workflows / "create-draft-release.yml").exists()
    assert is_valid_yaml(workflows / "main.yml")
    assert is_valid_yaml(workflows / "release.yml")
    assert "create-draft-release:" in main_workflow
    assert "needs: [ quality, tests ]" in main_workflow
    assert "--verify-tag" in main_workflow
    assert "workflow_dispatch" not in release_workflow
    assert "ref: ${{ github.event.release.tag_name }}" in release_workflow
    assert "gh release download" in release_workflow
    assert "make build" not in release_workflow
    assert "needs: [ quality, tests ]" in release_workflow


def test_generated_tox_uses_supported_version_requirement(cookies):
    result = cookies.bake()

    assert result.exit_code == 0, result.exception

    tox_config = (Path(result.project_path) / "tox.ini").read_text(encoding="utf-8")
    assert "requires = tox>=4" in tox_config
    assert "min_version" not in tox_config


def test_generated_metadata_uses_pep639_license_fields(cookies):
    result = cookies.bake()

    assert result.exit_code == 0, result.exception

    pyproject = tomli.loads((Path(result.project_path) / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]
    assert not any(classifier.startswith("License ::") for classifier in project["classifiers"])


def test_generated_pytest_keeps_deprecation_warnings_visible(cookies):
    result = cookies.bake()

    assert result.exit_code == 0, result.exception

    pyproject = tomli.loads((Path(result.project_path) / "pyproject.toml").read_text(encoding="utf-8"))
    pytest_config = pyproject["tool"]["pytest"]["ini_options"]
    assert "-p no:warnings" not in pytest_config["addopts"]
    assert "filterwarnings" not in pytest_config


def test_wheel_installs_documented_cli_name(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"project_name": "my-project"})
        project_path = Path(result.project_path)

        assert result.exit_code == 0, result.exception

        uv_exe = shutil.which("uv") or "uv"
        dist_path = tmp_path / "dist"
        venv_path = tmp_path / "wheel-venv"
        subprocess.run(
            [uv_exe, "build", "--wheel", "--out-dir", str(dist_path)],
            cwd=project_path,
            check=True,
        )
        wheel_path = next(dist_path.glob("*.whl"))
        subprocess.run(
            [uv_exe, "venv", "--python", sys.executable, str(venv_path)],
            check=True,
        )
        venv_python = venv_path / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        subprocess.run(
            [uv_exe, "pip", "install", "--python", str(venv_python), str(wheel_path)],
            check=True,
        )

        scripts_path = venv_path / ("Scripts" if sys.platform == "win32" else "bin")
        command_path = scripts_path / ("my-project.exe" if sys.platform == "win32" else "my-project")
        completed = subprocess.run(
            [str(command_path), "--help"],
            check=True,
            capture_output=True,
            text=True,
        )

        assert "Usage: my-project" in completed.stdout
        assert not (scripts_path / "my_project").exists()


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
