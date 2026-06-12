from itertools import combinations
import subprocess
from pathlib import Path


def parse_numstat_entries(output: str) -> list[dict[str, int | str]]:
    entries = []
    for line in output.splitlines():
        row = line.strip()
        if not row or row.startswith("commit "):
            continue
        added, deleted, path = row.split("\t", maxsplit=2)
        if added == "-" or deleted == "-":
            continue
        entries.append({"path": path, "added": int(added), "deleted": int(deleted)})
    return entries


def parse_commit_file_groups(output: str) -> list[list[str]]:
    groups = []
    current_group = []
    for line in output.splitlines():
        row = line.strip()
        if not row:
            continue
        if row.startswith("commit "):
            if current_group:
                groups.append(current_group)
            current_group = []
            continue
        current_group.append(row)

    if current_group:
        groups.append(current_group)
    return groups


def parse_author_entries(output: str) -> list[dict[str, str]]:
    entries = []
    for line in output.splitlines():
        row = line.strip()
        if not row:
            continue
        name, email = row.split("\t", maxsplit=1)
        entries.append({"name": name, "email": email})
    return entries


def list_numstat_entries(repo: Path) -> list[dict[str, int | str]]:
    try:
        result = subprocess.run(
            ["git", "log", "--numstat", "--pretty=format:commit %H"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return parse_numstat_entries(result.stdout)


def list_commit_file_groups(repo: Path) -> list[list[str]]:
    try:
        result = subprocess.run(
            ["git", "log", "--name-only", "--pretty=format:commit %H"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return parse_commit_file_groups(result.stdout)


def list_author_entries(repo: Path) -> list[dict[str, str]]:
    try:
        result = subprocess.run(
            ["git", "log", "--format=%an%x09%ae"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return parse_author_entries(result.stdout)


def aggregate_churn(
    entries: list[dict[str, int | str]],
) -> dict[str, dict[str, int]]:
    churn_by_path = {}
    for entry in entries:
        path = str(entry["path"])
        added = int(entry["added"])
        deleted = int(entry["deleted"])
        churn_by_path.setdefault(path, {"added": 0, "deleted": 0, "churn": 0})
        churn_by_path[path]["added"] += added
        churn_by_path[path]["deleted"] += deleted
        churn_by_path[path]["churn"] += added + deleted
    return churn_by_path


def count_cochange_pairs(groups: list[list[str]]) -> dict[tuple[str, str], int]:
    pair_counts = {}
    for group in groups:
        for left, right in combinations(sorted(set(group)), 2):
            pair_counts.setdefault((left, right), 0)
            pair_counts[(left, right)] += 1
    return pair_counts


def rank_cochanges(
    pair_counts: dict[tuple[str, str], int],
) -> list[dict[str, int | str]]:
    return [
        {"left": left, "right": right, "count": count}
        for (left, right), count in sorted(
            pair_counts.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
        )
    ]


def rank_churn(
    churn_by_path: dict[str, dict[str, int]],
) -> list[dict[str, int | str]]:
    return [
        {
            "path": path,
            "added": totals["added"],
            "deleted": totals["deleted"],
            "churn": totals["churn"],
        }
        for path, totals in sorted(
            churn_by_path.items(), key=lambda item: (-item[1]["churn"], item[0])
        )
    ]


def rank_authors(entries: list[dict[str, str]]) -> list[dict[str, int | str]]:
    authors = {}
    for entry in entries:
        key = (entry["name"], entry["email"])
        authors.setdefault(key, 0)
        authors[key] += 1

    return [
        {"name": name, "email": email, "commits": commits}
        for (name, email), commits in sorted(
            authors.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
        )
    ]


def find_churn_hotspots(repo: Path) -> list[dict[str, int | str]]:
    return rank_churn(aggregate_churn(list_numstat_entries(repo)))


def find_cochanges(repo: Path) -> list[dict[str, int | str]]:
    return rank_cochanges(count_cochange_pairs(list_commit_file_groups(repo)))


def find_repository_summary(repo: Path) -> dict[str, int]:
    entries = list_numstat_entries(repo)
    groups = list_commit_file_groups(repo)
    churn_by_path = aggregate_churn(entries)
    cochange_pairs = count_cochange_pairs(groups)

    return {
        "changed_files": len(churn_by_path),
        "cochange_pairs": len(cochange_pairs),
        "commits": len(groups),
        "total_added": sum(int(entry["added"]) for entry in entries),
        "total_churn": sum(totals["churn"] for totals in churn_by_path.values()),
        "total_deleted": sum(int(entry["deleted"]) for entry in entries),
    }


def find_authors(repo: Path) -> list[dict[str, int | str]]:
    return rank_authors(list_author_entries(repo))
