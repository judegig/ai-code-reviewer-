SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def remove_duplicates(issues: list) -> list:
    # Two issues are duplicates if they point to the same file and same line.
    seen = set()
    unique = []
    for issue in issues:
        key = (issue["file"], issue["line"])
        if key not in seen:
            seen.add(key)
            unique.append(issue)
    return unique


def sort_by_severity(issues: list) -> list:
    # high comes first (0), then medium (1), then low (2).
    return sorted(issues, key=lambda i: SEVERITY_ORDER.get(i["severity"], 99))


def group_by_file(issues: list) -> dict:
    # Returns {"filename": [issue, issue, ...], ...}
    grouped = {}
    for issue in issues:
        filename = issue["file"]
        if filename not in grouped:
            grouped[filename] = []
        grouped[filename].append(issue)
    return grouped


def coordinate(issues: list) -> dict:
    issues = remove_duplicates(issues)
    issues = sort_by_severity(issues)
    grouped = group_by_file(issues)
    return grouped
