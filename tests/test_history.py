import subprocess

from palm_tree.history import list_touched_files, parse_touched_files


def test_parse_touched_files_from_git_output():
    output = "README.md\nsrc/palm_tree/cli.py\n"

    assert parse_touched_files(output) == ["README.md", "src/palm_tree/cli.py"]


def test_parse_touched_files_ignores_commit_headers_and_blanks():
    output = "\ncommit abc123\nREADME.md\n\ncommit def456\nsrc/palm_tree/cli.py\n"

    assert parse_touched_files(output) == ["README.md", "src/palm_tree/cli.py"]


def test_list_touched_files_runs_git_log(monkeypatch, tmp_path):
    calls = []

    def fake_run(command, cwd, check, capture_output, text):
        calls.append(
            {
                "command": command,
                "cwd": cwd,
                "check": check,
                "capture_output": capture_output,
                "text": text,
            }
        )
        return subprocess.CompletedProcess(command, 0, stdout="README.md\n")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert list_touched_files(tmp_path) == ["README.md"]
    assert calls == [
        {
            "command": ["git", "log", "--name-only", "--pretty=format:commit %H"],
            "cwd": tmp_path,
            "check": True,
            "capture_output": True,
            "text": True,
        }
    ]
