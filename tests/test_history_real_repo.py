import subprocess

from palm_tree.history import (
    find_authors,
    find_churn_hotspots,
    find_cochanges,
    find_repository_summary,
    find_stale_files,
    list_tracked_files,
)


def _init_repo(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True
    )
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)


def test_list_tracked_files_returns_committed_files(tmp_path):
    _init_repo(tmp_path)

    (tmp_path / "a.py").write_text("a\n")
    (tmp_path / "b.py").write_text("b\n")
    subprocess.run(["git", "add", "a.py", "b.py"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Add files"], cwd=tmp_path, check=True)

    assert list_tracked_files(tmp_path) == {"a.py", "b.py"}


def test_find_repository_summary_on_empty_repository_is_all_zero(tmp_path):
    _init_repo(tmp_path)

    assert find_repository_summary(tmp_path) == {
        "authors": 0,
        "changed_files": 0,
        "cochange_pairs": 0,
        "commits": 0,
        "total_added": 0,
        "total_churn": 0,
        "total_deleted": 0,
        "tracked_files": 0,
    }


def test_find_authors_on_empty_repository_returns_empty_list(tmp_path):
    _init_repo(tmp_path)

    assert find_authors(tmp_path) == []


def test_find_churn_hotspots_on_empty_repository_returns_empty_list(tmp_path):
    _init_repo(tmp_path)

    assert find_churn_hotspots(tmp_path) == []


def test_find_cochanges_on_empty_repository_returns_empty_list(tmp_path):
    _init_repo(tmp_path)

    assert find_cochanges(tmp_path) == []


def test_find_stale_files_on_empty_repository_returns_empty_list(tmp_path):
    _init_repo(tmp_path)

    assert find_stale_files(tmp_path) == []
