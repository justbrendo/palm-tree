from palm_tree.history import (
    parse_author_entries,
    parse_commit_file_groups,
    parse_last_changed_entries,
    parse_numstat_entries,
)


def test_parse_numstat_entries_empty_string_returns_empty_list():
    assert parse_numstat_entries("") == []


def test_parse_numstat_entries_ignores_blank_lines():
    output = "10\t2\tREADME.md\n\n\n3\t1\tsrc/palm_tree/cli.py\n"

    assert parse_numstat_entries(output) == [
        {"path": "README.md", "added": 10, "deleted": 2},
        {"path": "src/palm_tree/cli.py", "added": 3, "deleted": 1},
    ]


def test_parse_commit_file_groups_empty_string_returns_empty_list():
    assert parse_commit_file_groups("") == []


def test_parse_commit_file_groups_ignores_blank_lines_between_files():
    output = "commit abc123\nREADME.md\n\nsrc/palm_tree/cli.py\n"

    assert parse_commit_file_groups(output) == [
        ["README.md", "src/palm_tree/cli.py"]
    ]


def test_parse_author_entries_empty_string_returns_empty_list():
    assert parse_author_entries("") == []


def test_parse_last_changed_entries_without_commit_prefix_returns_empty_list():
    assert parse_last_changed_entries("README.md\nsrc/palm_tree/cli.py\n") == []
