import subprocess

from palm_tree.history import (
    count_touched_files,
    find_hotspots,
    list_touched_files,
    parse_touched_files,
    rank_hotspots,
)


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


def test_count_touched_files_counts_each_path():
    touched_files = ["README.md", "src/palm_tree/cli.py", "README.md"]

    assert count_touched_files(touched_files) == {
        "README.md": 2,
        "src/palm_tree/cli.py": 1,
    }


def test_rank_hotspots_orders_files_by_touch_count():
    touch_counts = {
        "src/palm_tree/cli.py": 1,
        "README.md": 3,
        "tests/test_cli.py": 2,
    }

    assert rank_hotspots(touch_counts) == [
        {"path": "README.md", "touches": 3},
        {"path": "tests/test_cli.py", "touches": 2},
        {"path": "src/palm_tree/cli.py", "touches": 1},
    ]


def test_find_hotspots_lists_counts_and_ranks_files(monkeypatch, tmp_path):
    def fake_list_touched_files(repo):
        assert repo == tmp_path
        return ["README.md", "src/palm_tree/cli.py", "README.md"]

    monkeypatch.setattr("palm_tree.history.list_touched_files", fake_list_touched_files)

    assert find_hotspots(tmp_path) == [
        {"path": "README.md", "touches": 2},
        {"path": "src/palm_tree/cli.py", "touches": 1},
    ]
