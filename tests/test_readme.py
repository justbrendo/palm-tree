from pathlib import Path


def test_readme_explains_repository_mining_signals():
    readme = Path("README.md").read_text()

    assert "git history" in readme
    assert "churn hotspots" in readme
    assert "files that change together" in readme
    assert "stale files" in readme


def test_readme_documents_group_members():
    readme = Path("README.md").read_text()

    assert "## Group members" in readme
    assert "Brendo Gético Eugênio" in readme


def test_readme_documents_technology_stack():
    readme = Path("README.md").read_text()

    assert "## Technology stack" in readme
    assert "Python 3.14" in readme
    assert "Typer" in readme
    assert "pytest" in readme
    assert "GitHub Actions" in readme


def test_readme_documents_generative_ai_use():
    readme = Path("README.md").read_text()

    assert "## Generative AI use" in readme
    assert "AI coding agents" in readme
    assert "human instructions" in readme
    assert "reviewed, tested, and committed" in readme


def test_readme_shows_example_output():
    readme = Path("README.md").read_text()

    assert "## Example output" in readme
    assert "metric\tvalue" in readme
    assert "total_churn" in readme


def test_readme_documents_version_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree --version" in readme
    assert "palm-tree version" in readme


def test_readme_documents_local_checks():
    readme = Path("README.md").read_text()

    assert "python -m pytest" in readme
    assert "python -m pip wheel . --no-deps --wheel-dir dist" in readme


def test_readme_documents_release_status():
    readme = Path("README.md").read_text()

    assert "## v0.1 status" in readme
    assert "Core repository-mining commands are implemented" in readme
    assert "GitHub Actions runs tests and builds a wheel" in readme


def test_readme_documents_command_overview():
    readme = Path("README.md").read_text()

    assert "## Command overview" in readme
    assert "| `summary` | Repository-level metrics. |" in readme
    assert "| `hotspots` | Files ranked by churn. |" in readme
    assert "| `cochanges` | File pairs that change together. |" in readme


def test_readme_documents_summary_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree summary" in readme
    assert "palm-tree summary --repo /path/to/repository --json" in readme
    assert "tracked_files" in readme
    assert "authors" in readme
    assert "total_churn" in readme


def test_readme_documents_hotspots_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree hotspots" in readme
    assert "palm-tree hotspots --repo /path/to/repository --min-churn 10" in readme
    assert "palm-tree hotspots --repo /path/to/repository --json" in readme


def test_readme_documents_authors_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree authors" in readme
    assert "palm-tree authors --repo /path/to/repository --limit 5" in readme
    assert "palm-tree authors --repo /path/to/repository --json" in readme


def test_readme_documents_cochanges_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree cochanges" in readme
    assert "palm-tree cochanges --repo /path/to/repository --min-count 2" in readme
    assert "palm-tree cochanges --repo /path/to/repository --json" in readme


def test_readme_documents_stale_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree stale" in readme
    assert "palm-tree stale --repo /path/to/repository --limit 5" in readme
    assert "palm-tree stale --repo /path/to/repository --json" in readme
