import subprocess

from palm_tree.history import (
    aggregate_churn,
    count_cochange_pairs,
    find_cochanges,
    find_churn_hotspots,
    list_commit_file_groups,
    list_numstat_entries,
    parse_commit_file_groups,
    parse_numstat_entries,
    rank_cochanges,
    rank_churn,
)


def test_parse_numstat_entries_from_git_output():
    output = "\ncommit abc123\n10\t2\tREADME.md\n0\t4\tsrc/palm_tree/cli.py\n"

    assert parse_numstat_entries(output) == [
        {"path": "README.md", "added": 10, "deleted": 2},
        {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4},
    ]


def test_parse_numstat_entries_skips_binary_files():
    output = "10\t2\tREADME.md\n-\t-\tassets/logo.png\n"

    assert parse_numstat_entries(output) == [
        {"path": "README.md", "added": 10, "deleted": 2}
    ]


def test_parse_commit_file_groups_from_git_output():
    output = "\ncommit abc123\nREADME.md\nsrc/palm_tree/cli.py\n\ncommit def456\nREADME.md\n"

    assert parse_commit_file_groups(output) == [
        ["README.md", "src/palm_tree/cli.py"],
        ["README.md"],
    ]


def test_list_numstat_entries_runs_git_log(monkeypatch, tmp_path):
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
        return subprocess.CompletedProcess(command, 0, stdout="10\t2\tREADME.md\n")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert list_numstat_entries(tmp_path) == [
        {"path": "README.md", "added": 10, "deleted": 2}
    ]
    assert calls == [
        {
            "command": ["git", "log", "--numstat", "--pretty=format:commit %H"],
            "cwd": tmp_path,
            "check": True,
            "capture_output": True,
            "text": True,
        }
    ]


def test_list_numstat_entries_returns_empty_for_empty_history(monkeypatch, tmp_path):
    def fake_run(command, cwd, check, capture_output, text):
        raise subprocess.CalledProcessError(128, command)

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert list_numstat_entries(tmp_path) == []


def test_list_commit_file_groups_runs_git_log(monkeypatch, tmp_path):
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
        return subprocess.CompletedProcess(
            command, 0, stdout="commit abc123\nREADME.md\nsrc/palm_tree/cli.py\n"
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert list_commit_file_groups(tmp_path) == [
        ["README.md", "src/palm_tree/cli.py"]
    ]
    assert calls == [
        {
            "command": ["git", "log", "--name-only", "--pretty=format:commit %H"],
            "cwd": tmp_path,
            "check": True,
            "capture_output": True,
            "text": True,
        }
    ]


def test_list_commit_file_groups_returns_empty_for_empty_history(monkeypatch, tmp_path):
    def fake_run(command, cwd, check, capture_output, text):
        raise subprocess.CalledProcessError(128, command)

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert list_commit_file_groups(tmp_path) == []


def test_aggregate_churn_sums_lines_by_path():
    entries = [
        {"path": "README.md", "added": 10, "deleted": 2},
        {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4},
        {"path": "README.md", "added": 3, "deleted": 1},
    ]

    assert aggregate_churn(entries) == {
        "README.md": {"added": 13, "deleted": 3, "churn": 16},
        "src/palm_tree/cli.py": {"added": 0, "deleted": 4, "churn": 4},
    }


def test_count_cochange_pairs_counts_files_changed_together():
    groups = [
        ["README.md", "src/palm_tree/cli.py", "tests/test_cli.py"],
        ["tests/test_cli.py", "README.md"],
        ["README.md"],
    ]

    assert count_cochange_pairs(groups) == {
        ("README.md", "src/palm_tree/cli.py"): 1,
        ("README.md", "tests/test_cli.py"): 2,
        ("src/palm_tree/cli.py", "tests/test_cli.py"): 1,
    }


def test_rank_cochanges_orders_pairs_by_count():
    pair_counts = {
        ("src/palm_tree/cli.py", "tests/test_cli.py"): 1,
        ("README.md", "tests/test_cli.py"): 3,
        ("README.md", "src/palm_tree/cli.py"): 3,
    }

    assert rank_cochanges(pair_counts) == [
        {
            "left": "README.md",
            "right": "src/palm_tree/cli.py",
            "count": 3,
        },
        {
            "left": "README.md",
            "right": "tests/test_cli.py",
            "count": 3,
        },
        {
            "left": "src/palm_tree/cli.py",
            "right": "tests/test_cli.py",
            "count": 1,
        },
    ]


def test_rank_churn_orders_files_by_total_churn():
    churn_by_path = {
        "src/palm_tree/cli.py": {"added": 0, "deleted": 4, "churn": 4},
        "README.md": {"added": 13, "deleted": 3, "churn": 16},
        "tests/test_cli.py": {"added": 8, "deleted": 2, "churn": 10},
    }

    assert rank_churn(churn_by_path) == [
        {"path": "README.md", "added": 13, "deleted": 3, "churn": 16},
        {"path": "tests/test_cli.py", "added": 8, "deleted": 2, "churn": 10},
        {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
    ]


def test_find_churn_hotspots_lists_aggregates_and_ranks_files(monkeypatch, tmp_path):
    def fake_list_numstat_entries(repo):
        assert repo == tmp_path
        return [
            {"path": "README.md", "added": 10, "deleted": 2},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4},
            {"path": "README.md", "added": 3, "deleted": 1},
        ]

    monkeypatch.setattr(
        "palm_tree.history.list_numstat_entries", fake_list_numstat_entries
    )

    assert find_churn_hotspots(tmp_path) == [
        {"path": "README.md", "added": 13, "deleted": 3, "churn": 16},
        {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
    ]


def test_find_cochanges_lists_counts_and_ranks_pairs(monkeypatch, tmp_path):
    def fake_list_commit_file_groups(repo):
        assert repo == tmp_path
        return [
            ["README.md", "src/palm_tree/cli.py", "tests/test_cli.py"],
            ["tests/test_cli.py", "README.md"],
        ]

    monkeypatch.setattr(
        "palm_tree.history.list_commit_file_groups", fake_list_commit_file_groups
    )

    assert find_cochanges(tmp_path) == [
        {"left": "README.md", "right": "tests/test_cli.py", "count": 2},
        {"left": "README.md", "right": "src/palm_tree/cli.py", "count": 1},
        {
            "left": "src/palm_tree/cli.py",
            "right": "tests/test_cli.py",
            "count": 1,
        },
    ]
