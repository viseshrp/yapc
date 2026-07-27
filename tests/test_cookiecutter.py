from __future__ import annotations

import shutil
import subprocess
from datetime import date
from pathlib import Path

import pytest

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
