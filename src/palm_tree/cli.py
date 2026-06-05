from pathlib import Path

import typer


app = typer.Typer()


@app.callback()
def main():
    """Mine repositories for maintenance and evolution signals."""


@app.command()
def info(repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect.")):
    """Show repository information."""
