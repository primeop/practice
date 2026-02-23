"""
HTTP Log Parser - Solution with manual tests.
Run: python solution.py
"""


def parse_log_line(line: str):
    """Parse one log line. Returns dict with method, path, status or None if invalid."""
    line = line.strip()
    if not line:
        return None
    parts = line.split()
    if len(parts) != 3:
        return None
    method, path, status_str = parts
    if not status_str.isdigit():
        return None
    return {"method": method, "path": path, "status": int(status_str)}


def count_by_status(log_lines: list, status: int) -> int:
    """Count how many log lines have the given status code."""
    count = 0
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed and parsed["status"] == status:
            count += 1
    return count


def count_requests_to_path(log_lines: list, path: str) -> int:
    """Count requests to the given path (any method)."""
    count = 0
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed and parsed["path"] == path:
            count += 1
    return count


def most_requested_path(log_lines: list) -> str:
    """Return the path requested most often. Tie => return any one."""
    path_counts = {}
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed:
            p = parsed["path"]
            path_counts[p] = path_counts.get(p, 0) + 1
    if not path_counts:
        return ""
    return max(path_counts, key=lambda p: path_counts[p])


# ---------------------------------------------------------------------------
# Follow-ups (with clean commented examples)
# ---------------------------------------------------------------------------

def count_requests_to_path_with_method(log_lines: list, path: str, method: str = None) -> int:
    """
    F1: Count requests to path; if method is provided, count only that method.
    Example:
        count_requests_to_path_with_method(logs, "/api/users")           -> 3   # all methods
        count_requests_to_path_with_method(logs, "/api/users", "GET")   -> 3   # only GET
        count_requests_to_path_with_method(logs, "/api/orders", "POST")  -> 1
    """
    count = 0
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed and parsed["path"] == path:
            if method is None or parsed["method"] == method:
                count += 1
    return count


def top_requested_paths(log_lines: list, n: int) -> list:
    """
    F2: Return top n most requested paths (descending by count). Tie-break by path string.
    Example:
        top_requested_paths(logs, 1) -> ["/api/users"]
        top_requested_paths(logs, 2) -> ["/api/users", "/api/products"]  # or ["/api/users", "/api/orders"] by tie
    """
    path_counts = {}
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed:
            p = parsed["path"]
            path_counts[p] = path_counts.get(p, 0) + 1
    # Sort by count desc, then by path asc for tie-break
    sorted_paths = sorted(path_counts.items(), key=lambda x: (-x[1], x[0]))
    return [p for p, _ in sorted_paths[:n]]


def status_breakdown_by_path(log_lines: list, path: str) -> dict:
    """
    F4: Return {status_code: count} for all requests to that path.
    Example:
        status_breakdown_by_path(logs, "/api/users") -> {200: 2, 404: 1}
    """
    breakdown = {}
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed and parsed["path"] == path:
            s = parsed["status"]
            breakdown[s] = breakdown.get(s, 0) + 1
    return breakdown


def run_tests():
    logs = [
        "GET /api/users 200",
        "POST /api/orders 201",
        "GET /api/users 404",
        "GET /api/products 200",
        "GET /api/users 200",
    ]

    # parse_log_line
    assert parse_log_line("GET /api/users 200") == {"method": "GET", "path": "/api/users", "status": 200}
    assert parse_log_line("") is None
    assert parse_log_line("GET /api 200 200") is None
    assert parse_log_line("GET /api users") is None  # status not numeric

    # count_by_status
    assert count_by_status(logs, 200) == 3
    assert count_by_status(logs, 404) == 1
    assert count_by_status(logs, 500) == 0
    assert count_by_status([], 200) == 0

    # count_requests_to_path
    assert count_requests_to_path(logs, "/api/users") == 3
    assert count_requests_to_path(logs, "/api/orders") == 1
    assert count_requests_to_path(logs, "/other") == 0

    # most_requested_path
    assert most_requested_path(logs) == "/api/users"
    assert most_requested_path([]) == ""

    # Follow-ups
    assert count_requests_to_path_with_method(logs, "/api/users") == 3
    assert count_requests_to_path_with_method(logs, "/api/users", "GET") == 3
    assert count_requests_to_path_with_method(logs, "/api/orders", "POST") == 1
    assert top_requested_paths(logs, 1) == ["/api/users"]
    assert len(top_requested_paths(logs, 3)) == 3
    assert status_breakdown_by_path(logs, "/api/users") == {200: 2, 404: 1}

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
