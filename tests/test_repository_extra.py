import subprocess

from palm_tree.repository import is_git_repository


def test_detects_real_git_repository(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)

    assert is_git_repository(tmp_path)


def test_returns_false_when_git_executable_missing(monkeypatch, tmp_path):
    def fake_run(command, cwd, check, capture_output, text):
        raise FileNotFoundError("git not found")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert not is_git_repository(tmp_path)


def test_returns_false_for_plain_directory(tmp_path):
    nested = tmp_path / "not_a_repo"
    nested.mkdir()

    assert not is_git_repository(nested)
