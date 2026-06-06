import subprocess
from collections import Counter
from pathlib import Path


def parse_touched_files(output: str) -> list[str]:
    touched_files = []
    for line in output.splitlines():
        path = line.strip()
        if not path or path.startswith("commit "):
            continue
        touched_files.append(path)
    return touched_files


def parse_numstat_entries(output: str) -> list[dict[str, int | str]]:
    entries = []
    for line in output.splitlines():
        row = line.strip()
        if not row or row.startswith("commit "):
            continue
        added, deleted, path = row.split("\t", maxsplit=2)
        entries.append({"path": path, "added": int(added), "deleted": int(deleted)})
    return entries


def list_touched_files(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "log", "--name-only", "--pretty=format:commit %H"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return parse_touched_files(result.stdout)


def list_numstat_entries(repo: Path) -> list[dict[str, int | str]]:
    result = subprocess.run(
        ["git", "log", "--numstat", "--pretty=format:commit %H"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return parse_numstat_entries(result.stdout)


def count_touched_files(touched_files: list[str]) -> dict[str, int]:
    return dict(Counter(touched_files))


def rank_hotspots(touch_counts: dict[str, int]) -> list[dict[str, int | str]]:
    return [
        {"path": path, "touches": touches}
        for path, touches in sorted(
            touch_counts.items(), key=lambda item: (-item[1], item[0])
        )
    ]


def find_hotspots(repo: Path) -> list[dict[str, int | str]]:
    return rank_hotspots(count_touched_files(list_touched_files(repo)))
