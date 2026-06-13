from pathlib import Path


def test_changelog_documents_initial_release_scope():
    changelog = Path("CHANGELOG.md").read_text()

    assert "## 0.1.0" in changelog
    assert "summary" in changelog
    assert "tracked files" in changelog
    assert "hotspots" in changelog
    assert "authors" in changelog
    assert "cochanges" in changelog
    assert "stale" in changelog
    assert "GitHub Actions" in changelog
