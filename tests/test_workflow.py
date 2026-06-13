from pathlib import Path


def test_ci_verifies_console_script():
    workflow = Path(".github/workflows/tests.yml").read_text()

    assert "palm-tree --version" in workflow


def test_ci_builds_wheel():
    workflow = Path(".github/workflows/tests.yml").read_text()

    assert "python -m pip wheel . --no-deps --wheel-dir dist" in workflow
