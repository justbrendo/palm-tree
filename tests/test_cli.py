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
