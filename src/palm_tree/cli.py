from pathlib import Path

import typer

from palm_tree.history import find_hotspots
from palm_tree.repository import is_git_repository


app = typer.Typer()


@app.callback()
def main():
    """Mine repositories for maintenance and evolution signals."""


@app.command()
def info(repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect.")):
    """Show repository information."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    typer.echo("Git repository: yes")


@app.command()
def hotspots(
    repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect."),
    limit: int = typer.Option(10, "--limit", help="Maximum number of hotspots to show."),
):
    """Show files with the most repository churn."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    for hotspot in find_hotspots(repo)[:limit]:
        typer.echo(f"{hotspot['touches']}\t{hotspot['path']}")
