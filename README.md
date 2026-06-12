# palm-tree
CLI tools capable of identifying problems relevant to code maintenance and evolution

## Development setup

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

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

The `summary` command reports `commits`, `changed_files`, `cochange_pairs`,
`total_added`, `total_deleted`, and `total_churn`.

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
