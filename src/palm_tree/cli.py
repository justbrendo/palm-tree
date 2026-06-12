import json
from importlib.metadata import version as package_version
from pathlib import Path

import typer

from palm_tree.history import find_churn_hotspots, find_cochanges, find_repository_summary
from palm_tree.repository import is_git_repository


app = typer.Typer()


@app.callback()
def main():
    """Mine repositories for maintenance and evolution signals."""


@app.command()
def version():
    """Show the palm-tree version."""
    typer.echo(f"palm-tree {package_version('palm-tree')}")


@app.command()
def info(repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect.")):
    """Show repository information."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    typer.echo("Git repository: yes")


@app.command()
def summary(
    repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect."),
    as_json: bool = typer.Option(False, "--json", help="Print summary as JSON."),
):
    """Show repository mining summary metrics."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    summary = find_repository_summary(repo)
    if as_json:
        typer.echo(json.dumps(summary))
        return

    typer.echo("metric\tvalue")
    for metric, value in summary.items():
        typer.echo(f"{metric}\t{value}")


@app.command()
def hotspots(
    repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect."),
    limit: int = typer.Option(
        10, "--limit", min=1, help="Maximum number of hotspots to show."
    ),
    min_churn: int = typer.Option(
        0, "--min-churn", min=0, help="Minimum churn value to show."
    ),
    as_json: bool = typer.Option(False, "--json", help="Print hotspots as JSON."),
):
    """Show files with the most repository churn."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    hotspots = [
        hotspot
        for hotspot in find_churn_hotspots(repo)
        if int(hotspot["churn"]) >= min_churn
    ][:limit]
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
    min_count: int = typer.Option(
        1, "--min-count", min=1, help="Minimum shared commit count to show."
    ),
    as_json: bool = typer.Option(False, "--json", help="Print cochanges as JSON."),
):
    """Show files that tend to change together."""
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)

    cochanges = [
        cochange
        for cochange in find_cochanges(repo)
        if int(cochange["count"]) >= min_count
    ][:limit]
    if as_json:
        typer.echo(json.dumps(cochanges))
        return

    if not cochanges:
        typer.echo("No cochanges found.")
        return

    typer.echo("count\tleft\tright")
    for cochange in cochanges:
        typer.echo(f"{cochange['count']}\t{cochange['left']}\t{cochange['right']}")
