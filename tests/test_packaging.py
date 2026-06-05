import tomllib
from pathlib import Path


def test_console_script_is_configured():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    assert pyproject["project"]["scripts"]["palm-tree"] == "palm_tree.cli:app"
