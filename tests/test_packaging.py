import tomllib
from pathlib import Path


def test_console_script_is_configured():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    assert pyproject["project"]["scripts"]["palm-tree"] == "palm_tree.cli:app"


def test_project_metadata_is_release_ready():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    project = pyproject["project"]

    assert project["readme"] == "README.md"
    assert project["requires-python"] == ">=3.14"
    assert project["license"] == "MIT"
