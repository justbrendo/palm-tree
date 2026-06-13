import json
from importlib.metadata import version as package_version
from pathlib import Path

import typer

from palm_tree.history import (
    find_authors,
    find_churn_hotspots,
    find_cochanges,
    find_repository_summary,
    find_stale_files,
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


def _echo_rows(
    rows: list[dict[str, object]],
    headers: tuple[str, ...],
    empty_message: str,
    as_json: bool,
):
    if as_json:
        typer.echo(json.dumps(rows))
        return

    if not rows:
        typer.echo(empty_message)
        return

    _echo_table(
        headers,
        [tuple(row[header] for header in headers) for row in rows],
    )


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
    _echo_rows(
        hotspots,
        ("churn", "added", "deleted", "path"),
        "No hotspots found.",
        as_json,
    )


@app.command()
def authors(
    repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect."),
    limit: int = typer.Option(
        10, "--limit", min=1, help="Maximum number of authors to show."
    ),
    as_json: bool = typer.Option(False, "--json", help="Print authors as JSON."),
):
    """Show commit authors ranked by commit count."""
    _require_git_repository(repo)

    authors = find_authors(repo)[:limit]
    _echo_rows(authors, ("commits", "name", "email"), "No authors found.", as_json)


@app.command()
def stale(
    repo: Path = typer.Option(Path("."), "--repo", help="Repository path to inspect."),
    limit: int = typer.Option(
        10, "--limit", min=1, help="Maximum number of stale files to show."
    ),
    as_json: bool = typer.Option(False, "--json", help="Print stale files as JSON."),
):
    """Show files ordered by oldest last change."""
    _require_git_repository(repo)

    stale_files = find_stale_files(repo)[:limit]
    _echo_rows(
        stale_files,
        ("last_changed", "path"),
        "No stale files found.",
        as_json,
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
    _echo_rows(cochanges, ("count", "left", "right"), "No cochanges found.", as_json)
