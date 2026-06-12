import json
from importlib.metadata import version as package_version
from pathlib import Path

import typer

from palm_tree.history import (
    find_churn_hotspots,
    find_cochanges,
    find_repository_summary,
)
from palm_tree.repository import is_git_repository


app = typer.Typer()


def _require_git_repository(repo: Path):
    if not is_git_repository(repo):
        typer.echo(f"Error: {repo} is not a git repository.", err=True)
        raise typer.Exit(code=1)


def _echo_table(headers: tuple[str, ...], rows: list[tuple[object, ...]]):
    typer.echo("\t".join(headers))
    for row in rows:
        typer.echo("\t".join(str(value) for value in row))


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
    _require_git_repository(repo)

    typer.echo("Git repository: yes")


@app.command()
def summary(
    repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect."),
    as_json: bool = typer.Option(False, "--json", help="Print summary as JSON."),
):
    """Show repository mining summary metrics."""
    _require_git_repository(repo)

    summary = find_repository_summary(repo)
    if as_json:
        typer.echo(json.dumps(summary))
        return

    _echo_table(("metric", "value"), list(summary.items()))


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
    _require_git_repository(repo)

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

    _echo_table(
        ("churn", "added", "deleted", "path"),
        [
            (
                hotspot["churn"],
                hotspot["added"],
                hotspot["deleted"],
                hotspot["path"],
            )
            for hotspot in hotspots
        ],
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
    _require_git_repository(repo)

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

    _echo_table(
        ("count", "left", "right"),
        [
            (cochange["count"], cochange["left"], cochange["right"])
            for cochange in cochanges
        ],
    )
