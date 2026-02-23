# Practice 1: HTTP Request Log Parser

**Why this:** The doc says one question may be structured around HTTP requests; this practices that and clean, testable code.

## Problem

You're given a list of HTTP request log lines. Each line has this format (space-separated):

```
METHOD PATH STATUS_CODE
```

Example:
```
GET /api/users 200
POST /api/orders 201
GET /api/users 404
GET /api/products 200
GET /api/users 200
```

Implement:

1. **`parse_log_line(line: str) -> dict`**  
   Parse one line and return a dict with keys `method`, `path`, `status`.  
   If the line is invalid (wrong number of parts, non-numeric status), return `None`.

2. **`count_by_status(log_lines: list[str], status: int) -> int`**  
   Return how many log lines have the given status code.

3. **`count_requests_to_path(log_lines: list[str], path: str) -> int`**  
   Return how many requests were made to the given path (any method).

4. **`most_requested_path(log_lines: list[str]) -> str`**  
   Return the path that was requested most often. If tie, return any one of them.

**Edge cases to consider:** empty list, invalid lines, empty path, single line.

Write your own tests (e.g. in `main` or a small test block) that check these functions.

---

## Possible follow-ups (practice extending your solution)

- **F1 — Filter by method:** `count_requests_to_path(log_lines, path, method=None)`. If `method` is provided (e.g. `"GET"`), count only requests with that method to the path.
- **F2 — Top N paths:** `top_requested_paths(log_lines: list, n: int) -> list[str]`. Return the top `n` most requested paths (descending by count). Tie-break by path string order if needed.
- **F3 — Logs in time window:** Assume each log line can include an optional timestamp at the end: `METHOD PATH STATUS [timestamp]`. Add `count_by_status_in_window(log_lines, status, start_ts, end_ts)` that only counts lines with timestamp in `[start_ts, end_ts]`.
- **F4 — Status breakdown by path:** `status_breakdown_by_path(log_lines: list, path: str) -> dict[int, int]`. Return `{status_code: count}` for all requests to that path (e.g. `{200: 3, 404: 1}`).

**Implemented in solution.py:** `count_requests_to_path_with_method` (F1), `top_requested_paths` (F2), `status_breakdown_by_path` (F4). F3 (time window) is optional — extend `parse_log_line` to accept optional timestamp.
