def parse_touched_files(output: str) -> list[str]:
    return [line for line in output.splitlines() if line.strip()]
