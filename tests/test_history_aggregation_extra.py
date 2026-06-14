from palm_tree.history import (
    aggregate_churn,
    count_cochange_pairs,
    rank_authors,
    rank_churn,
    rank_cochanges,
    rank_stale_files,
)


def test_aggregate_churn_with_no_entries_returns_empty_dict():
    assert aggregate_churn([]) == {}


def test_count_cochange_pairs_with_no_groups_returns_empty_dict():
    assert count_cochange_pairs([]) == {}


def test_count_cochange_pairs_ignores_single_file_groups():
    groups = [["README.md"], ["README.md"]]

    assert count_cochange_pairs(groups) == {}


def test_rank_churn_with_no_entries_returns_empty_list():
    assert rank_churn({}) == []


def test_rank_authors_with_no_entries_returns_empty_list():
    assert rank_authors([]) == []


def test_rank_cochanges_with_no_pairs_returns_empty_list():
    assert rank_cochanges({}) == []


def test_rank_stale_files_with_no_entries_returns_empty_list():
    assert rank_stale_files([]) == []


def test_rank_churn_breaks_ties_alphabetically():
    churn_by_path = {
        "b.py": {"added": 1, "deleted": 1, "churn": 2},
        "a.py": {"added": 1, "deleted": 1, "churn": 2},
    }

    assert rank_churn(churn_by_path) == [
        {"path": "a.py", "added": 1, "deleted": 1, "churn": 2},
        {"path": "b.py", "added": 1, "deleted": 1, "churn": 2},
    ]
