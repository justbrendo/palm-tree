# Changelog

## 0.1.0

Initial repository-mining CLI milestone.

### Added

- `palm-tree info` to validate and report git repository status.
- `palm-tree version` to show the installed package version.
- `palm-tree summary` for repository-level metrics: authors, commits, changed
  files, tracked files, cochange pairs, added lines, deleted lines, and total
  churn.
- `palm-tree hotspots` to rank files by git-history churn, with `--limit`,
  `--min-churn`, and `--json` output.
- `palm-tree authors` to rank commit authors by commit count, with `--limit`
  and `--json` output.
- `palm-tree stale` to rank files by oldest last-change date, with `--limit`
  and `--json` output.
- `palm-tree cochanges` to rank file pairs that change together, with `--limit`,
  `--min-count`, and `--json` output.
- Friendly errors for non-git repository paths.
- GitHub Actions test workflow for pushes and pull requests to `main`.
- Test coverage for parser behavior, CLI output, real git repositories, README
  usage, and packaging.
