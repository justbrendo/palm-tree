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


def test_info_command_accepts_repo_option(tmp_path):
    (tmp_path / ".git").mkdir()

    result = runner.invoke(app, ["info", "--repo", str(tmp_path)])

    assert result.exit_code == 0


def test_info_command_reports_git_repository(tmp_path):
    (tmp_path / ".git").mkdir()

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
