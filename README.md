# palm-tree

CLI tools for mining git history for maintenance and evolution signals.
`palm-tree` helps identify churn hotspots, files that change together, stale files,
and repository-level activity metrics.

## Group members

- Brendo Gético Eugênio

## Technology stack

- Python 3.14 for the CLI and repository-mining logic.
- Typer for command-line interface structure.
- pytest for automated tests.
- Git and subprocess-based repository mining.
- GitHub Actions for continuous integration.
- setuptools for packaging and console script configuration.

## Generative AI use

Generative AI coding agents were used during this project to write code,
tests, documentation, and repository updates directed by human instructions.
The development process remained human-led.
Requested changes were reviewed, tested, and committed in small increments.

## Example output

```text
$ palm-tree summary
metric	value
authors	2
commits	12
changed_files	8
total_churn	340
```

## Development setup

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run checks

```bash
python -m pytest
python -m pip wheel . --no-deps --wheel-dir dist
```

## v0.1 status

Core repository-mining commands are implemented for repository summaries,
churn hotspots, commit authors, stale files, and co-change pairs.

GitHub Actions runs tests and builds a wheel for pushes and pull requests to
`main`.

## Command overview

| Command | Purpose |
| --- | --- |
| `info` | Validate and report git repository status. |
| `summary` | Repository-level metrics. |
| `hotspots` | Files ranked by churn. |
| `authors` | Commit authors ranked by commit count. |
| `stale` | Tracked files ordered by oldest last change. |
| `cochanges` | File pairs that change together. |

## Usage

Show basic repository information for the current directory:

```bash
palm-tree info
```

Inspect another repository path:

```bash
palm-tree info --repo /path/to/repository
```

The `info` command exits with an error when the target path is not a git repository.

Show the installed CLI version:

```bash
palm-tree --version
palm-tree version
```

Show repository-level mining metrics:

```bash
palm-tree summary
```

Print summary metrics as JSON:

```bash
palm-tree summary --repo /path/to/repository --json
```

The `summary` command reports `authors`, `commits`, `changed_files`,
`cochange_pairs`, `tracked_files`, `total_added`, `total_deleted`, and
`total_churn`.

Show files with the most git-history churn:

```bash
palm-tree hotspots
```

Limit the number of hotspot rows:

```bash
palm-tree hotspots --repo /path/to/repository --limit 5
```

Show only files with churn of at least 10:

```bash
palm-tree hotspots --repo /path/to/repository --min-churn 10
```

Print hotspot rows as JSON:

```bash
palm-tree hotspots --repo /path/to/repository --json
```

The `hotspots` command prints churn, added lines, deleted lines, and file paths.
Churn is the sum of added and deleted lines. JSON output uses the same `churn`,
`added`, `deleted`, and `path` fields.

Show commit authors ranked by commit count:

```bash
palm-tree authors
```

Limit the number of author rows:

```bash
palm-tree authors --repo /path/to/repository --limit 5
```

Print author rows as JSON:

```bash
palm-tree authors --repo /path/to/repository --json
```

The `authors` command prints commit counts, author names, and author email
addresses. JSON output uses the same `commits`, `name`, and `email` fields.

Show tracked files ordered by oldest last change:

```bash
palm-tree stale
```

Limit the number of stale-file rows:

```bash
palm-tree stale --repo /path/to/repository --limit 5
```

Print stale-file rows as JSON:

```bash
palm-tree stale --repo /path/to/repository --json
```

The `stale` command prints the last git commit date and file path for each
tracked file. JSON output uses the same `last_changed` and `path` fields.

Show files that tend to change together in commits:

```bash
palm-tree cochanges
```

Limit the number of cochange rows:

```bash
palm-tree cochanges --repo /path/to/repository --limit 5
```

Show only pairs that changed together at least twice:

```bash
palm-tree cochanges --repo /path/to/repository --min-count 2
```

Print cochange rows as JSON:

```bash
palm-tree cochanges --repo /path/to/repository --json
```

The `cochanges` command prints the number of shared commits and the two file
paths in each pair. JSON output uses the same `count`, `left`, and `right`
fields.
