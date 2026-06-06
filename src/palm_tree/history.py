def parse_touched_files(output: str) -> list[str]:
    touched_files = []
    for line in output.splitlines():
        path = line.strip()
        if not path or path.startswith("commit "):
            continue
        touched_files.append(path)
    return touched_files
