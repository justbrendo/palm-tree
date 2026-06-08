from pathlib import Path


def test_readme_documents_cochanges_usage():
    readme = Path("README.md").read_text()

    assert "palm-tree cochanges" in readme
    assert "palm-tree cochanges --repo /path/to/repository --min-count 2" in readme
    assert "palm-tree cochanges --repo /path/to/repository --json" in readme
