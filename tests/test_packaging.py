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
    assert "Environment :: Console" in project["classifiers"]
    assert "Intended Audience :: Developers" in project["classifiers"]
    assert "Programming Language :: Python :: 3.14" in project["classifiers"]
    assert "Topic :: Software Development :: Quality Assurance" in project["classifiers"]
    assert project["urls"]["Repository"] == "https://github.com/justbrendo/palm-tree"
    assert project["urls"]["Issues"] == "https://github.com/justbrendo/palm-tree/issues"
