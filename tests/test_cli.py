import json
import subprocess

import typer
from typer.testing import CliRunner

from palm_tree.cli import app


runner = CliRunner()


def test_cli_app_is_typer_app():
    assert isinstance(app, typer.Typer)


def test_cli_app_can_show_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Mine repositories for maintenance and evolution signals." in result.output


def test_info_command_exists():
    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0


def test_info_command_has_repo_option():
    result = runner.invoke(app, ["info", "--help"])

    assert result.exit_code == 0
    assert "--repo" in result.output


def test_info_command_accepts_repo_option(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)

    result = runner.invoke(app, ["info", "--repo", str(tmp_path)])

    assert result.exit_code == 0


def test_info_command_reports_git_repository(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)

    result = runner.invoke(app, ["info", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "Git repository: yes" in result.output


def test_info_command_rejects_non_git_directory(tmp_path):
    result = runner.invoke(app, ["info", "--repo", str(tmp_path)])

    assert result.exit_code == 1
    assert "not a git repository" in result.output


def test_hotspots_command_exists():
    result = runner.invoke(app, ["hotspots"])

    assert result.exit_code == 0


def test_hotspots_command_has_repo_option():
    result = runner.invoke(app, ["hotspots", "--help"])

    assert result.exit_code == 0
    assert "--repo" in result.output


def test_hotspots_command_has_limit_option():
    result = runner.invoke(app, ["hotspots", "--help"])

    assert result.exit_code == 0
    assert "--limit" in result.output


def test_hotspots_command_has_json_option():
    result = runner.invoke(app, ["hotspots", "--help"])

    assert result.exit_code == 0
    assert "--json" in result.output


def test_hotspots_command_accepts_repo_option(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_churn_hotspots", lambda repo: [])

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0


def test_hotspots_command_reports_no_hotspots(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_churn_hotspots", lambda repo: [])

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "No hotspots found." in result.output


def test_hotspots_command_rejects_non_git_directory(tmp_path):
    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 1
    assert "not a git repository" in result.output


def test_hotspots_command_prints_ranked_files(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "churn\tadded\tdeleted\tpath" in result.output
    assert "12\t10\t2\tREADME.md" in result.output
    assert "4\t0\t4\tsrc/palm_tree/cli.py" in result.output


def test_hotspots_command_limits_output(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "tests/test_cli.py", "added": 4, "deleted": 2, "churn": 6},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path), "--limit", "2"])

    assert result.exit_code == 0
    assert "12\t10\t2\tREADME.md" in result.output
    assert "6\t4\t2\ttests/test_cli.py" in result.output
    assert "4\t0\t4\tsrc/palm_tree/cli.py" not in result.output


def test_hotspots_command_prints_json(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr(
        "palm_tree.cli.find_churn_hotspots",
        lambda repo: [
            {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
            {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
        ],
    )

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == [
        {"path": "README.md", "added": 10, "deleted": 2, "churn": 12},
        {"path": "src/palm_tree/cli.py", "added": 0, "deleted": 4, "churn": 4},
    ]


def test_hotspots_command_prints_empty_json(monkeypatch, tmp_path):
    monkeypatch.setattr("palm_tree.cli.is_git_repository", lambda repo: True)
    monkeypatch.setattr("palm_tree.cli.find_churn_hotspots", lambda repo: [])

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output) == []


def test_hotspots_command_reads_real_git_history(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    readme.write_text("hello\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Add readme"], cwd=tmp_path, check=True)

    readme.write_text("hello\nworld\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Update readme"], cwd=tmp_path, check=True)

    result = runner.invoke(app, ["hotspots", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert "churn\tadded\tdeleted\tpath" in result.output
    assert "2\t2\t0\tREADME.md" in result.output
