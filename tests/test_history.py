from palm_tree.history import parse_touched_files


def test_parse_touched_files_from_git_output():
    output = "README.md\nsrc/palm_tree/cli.py\n"

    assert parse_touched_files(output) == ["README.md", "src/palm_tree/cli.py"]
