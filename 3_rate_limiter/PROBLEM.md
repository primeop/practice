# Practice 3: Simple Rate Limiter

**Why this:** Practical problem you might see at a payments company: limit how often a client can do something in a time window.

## Problem

Implement a **per-user rate limiter** that allows at most **N requests** per user in any **T-second** sliding window.

You don't need to implement a real clock. Instead, you get a list of events:

- Each event is `(user_id: str, timestamp_seconds: int)`.
- Events are **sorted by timestamp** (ascending).
- For each event, you must say whether the request is **allowed** or **rate limited**.

**Rules:**
- Allow a request if, for that user, the number of requests in the time window `[timestamp - T, timestamp]` (inclusive) is **≤ N** before counting this request.
- So: when you see `(user_id, ts)`, count how many events for that user have timestamp in `[ts - T, ts]` (including events at exactly `ts` that you've already processed). If that count is already `N`, this new request is **rate limited**. Otherwise it's **allowed**.

**Interface:**

- **`process_events(events: list[tuple[str, int]], N: int, T: int) -> list[str]`**  
  For each event, append `"allowed"` or `"rate_limited"` to the result list (same order as events).

**Example:**

- `N = 2`, `T = 5`
- Events: `[("u1", 0), ("u1", 1), ("u1", 2), ("u2", 3), ("u1", 6)]`
- For `("u1", 0)`: 0 requests in [−5, 0] → **allowed**.  
- For `("u1", 1)`: 2 in [−4, 1] → **allowed**.  
- For `("u1", 2)`: 3 in [−3, 2] → **rate_limited**.  
- For `("u2", 3)`: 1 in [−2, 3] → **allowed**.  
- For `("u1", 6)`: window [1, 6]. Only **allowed** requests count toward the limit. So far in window we have (u1,1) only; (u1,2) was rate-limited so it doesn't count. So 1 < 2 → **allowed**.

**Convention:** Only requests that were **allowed** count toward the limit (rate-limited requests do not consume the quota).

Example output: `["allowed", "allowed", "rate_limited", "allowed", "allowed"]`.

Implement this and add a few tests (including edge cases: T=0, one user, many users).

---

## Possible follow-ups (practice extending your solution)

- **F1 — Remaining quota:** Change return type to include remaining quota. E.g. `process_events_with_quota(events, N, T) -> list[tuple[str, int]]` where each element is `("allowed"|"rate_limited", remaining_quota)`. For "allowed", remaining = N - count_after_this; for "rate_limited", remaining = 0 (or same as before).
- **F2 — Per-tier limits:** Different users have different limits. `process_events(events, get_limit: Callable[[str], int], T: int)`. `get_limit(user_id)` returns N for that user (e.g. premium=10, free=2). Same sliding-window logic, but N is per user.
- **F3 — Per-resource limit:** Rate limit by `(user_id, resource_id)`. Events become `(user_id, resource_id, timestamp)`. Allow at most N requests per (user, resource) in window T.
- **F4 — Return which request was limited:** Instead of just "allowed"/"rate_limited", return the 1-based index of the first event in the window that “consumed” the quota (or 0 if allowed and no previous in window). Helps debugging.

**Implemented in solution.py:** `process_events_with_quota` (F1) returns `(outcome, remaining_quota)`; `process_events_per_tier` (F2) takes `get_limit(user_id)` and `T`. F3 (per-resource) and F4 are optional extensions.
