from pathlib import Path


def test_readme_documents_summary_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree summary" in readme
    assert "palm-tree summary --repo /path/to/repository --json" in readme
    assert "total_churn" in readme


def test_readme_documents_hotspots_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree hotspots" in readme
    assert "palm-tree hotspots --repo /path/to/repository --min-churn 10" in readme
    assert "palm-tree hotspots --repo /path/to/repository --json" in readme


def test_readme_documents_cochanges_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree cochanges" in readme
    assert "palm-tree cochanges --repo /path/to/repository --min-count 2" in readme
    assert "palm-tree cochanges --repo /path/to/repository --json" in readme
