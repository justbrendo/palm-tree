import subprocess

from palm_tree.repository import is_git_repository


def test_detects_git_repository(monkeypatch, tmp_path):
    def fake_run(command, cwd, check, capture_output, text):
        assert command == ["git", "rev-parse", "--is-inside-work-tree"]
        assert cwd == tmp_path
        assert check is True
        assert capture_output is True
        assert text is True
        return subprocess.CompletedProcess(command, 0, stdout="true\n")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert is_git_repository(tmp_path)


def test_detects_non_git_directory(monkeypatch, tmp_path):
    def fake_run(command, cwd, check, capture_output, text):
        raise subprocess.CalledProcessError(128, command)

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert not is_git_repository(tmp_path)


def test_detects_missing_path_as_non_git_repository(tmp_path):
    assert not is_git_repository(tmp_path / "missing")
