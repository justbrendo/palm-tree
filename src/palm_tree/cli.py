from pathlib import Path

import typer

from palm_tree.repository import is_git_repository


app = typer.Typer()


@app.callback()
def main():
    """Mine repositories for maintenance and evolution signals."""


@app.command()
def info(repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect.")):
    """Show repository information."""
    git_status = "yes" if is_git_repository(repo) else "no"
    typer.echo(f"Git repository: {git_status}")
