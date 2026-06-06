from palm_tree.repository import is_git_repository


def test_detects_git_repository(tmp_path):
    (tmp_path / ".git").mkdir()

    assert is_git_repository(tmp_path)


def test_detects_non_git_directory(tmp_path):
    assert not is_git_repository(tmp_path)
