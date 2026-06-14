from typer.testing import CliRunner

from palm_tree.cli import app


runner = CliRunner()


def test_version_command_has_help():
    result = runner.invoke(app, ["version", "--help"])

    assert result.exit_code == 0
    assert "Show the palm-tree version." in result.output


def test_info_command_has_help_description():
    result = runner.invoke(app, ["info", "--help"])

    assert result.exit_code == 0
    assert "Show repository information." in result.output


def test_summary_command_has_help_description():
    result = runner.invoke(app, ["summary", "--help"])

    assert result.exit_code == 0
    assert "Show repository mining summary metrics." in result.output


def test_unknown_command_fails():
    result = runner.invoke(app, ["does-not-exist"])

    assert result.exit_code != 0


def test_cli_help_lists_all_commands():
    result = runner.invoke(
        app,
        ["--help"],
        env={"COLUMNS": "120", "NO_COLOR": "1", "TERM": "dumb"},
    )

    assert result.exit_code == 0
    for command in ("info", "summary", "hotspots", "authors", "stale", "cochanges", "version"):
        assert command in result.output
