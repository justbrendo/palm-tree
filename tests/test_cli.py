import typer

from palm_tree.cli import app


def test_cli_app_is_typer_app():
    assert isinstance(app, typer.Typer)
