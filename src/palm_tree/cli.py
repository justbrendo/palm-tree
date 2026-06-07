import json
from pathlib import Path

import typer

from palm_tree.history import find_churn_hotspots, find_cochanges
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
    limit: int = typer.Option(
        10, "--limit", min=1, help="Maximum number of hotspots to show."
    ),
    as_json: bool = typer.Option(False, "--json", help="Print hotspots as JSON."),
):
    """Show files with the most repository churn."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    hotspots = find_churn_hotspots(repo)[:limit]
    if as_json:
        typer.echo(json.dumps(hotspots))
        return

    if not hotspots:
        typer.echo("No hotspots found.")
        return

    typer.echo("churn\tadded\tdeleted\tpath")
    for hotspot in hotspots:
        typer.echo(
            f"{hotspot['churn']}\t{hotspot['added']}\t"
            f"{hotspot['deleted']}\t{hotspot['path']}"
        )


@app.command()
def cochanges(
    repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect."),
    limit: int = typer.Option(
        10, "--limit", min=1, help="Maximum number of cochanges to show."
    ),
):
    """Show files that tend to change together."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    cochanges = find_cochanges(repo)[:limit]
    if not cochanges:
        typer.echo("No cochanges found.")
        return

    typer.echo("count\tleft\tright")
    for cochange in cochanges:
        typer.echo(f"{cochange['count']}\t{cochange['left']}\t{cochange['right']}")
