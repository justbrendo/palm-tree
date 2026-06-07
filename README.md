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

Show files with the most git-history churn:

```bash
palm-tree hotspots
```

Limit the number of hotspot rows:

```bash
palm-tree hotspots --repo /path/to/repository --limit 5
```

Print hotspot rows as JSON:

```bash
palm-tree hotspots --repo /path/to/repository --json
```

The `hotspots` command prints churn, added lines, deleted lines, and file paths.
Churn is the sum of added and deleted lines. JSON output uses the same `churn`,
`added`, `deleted`, and `path` fields.
