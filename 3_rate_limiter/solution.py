"""
Simple Rate Limiter - Solution with manual tests.
Run: python solution.py
"""


def process_events(events: list, N: int, T: int) -> list:
    """
    For each (user_id, timestamp), return "allowed" or "rate_limited".
    Allow if count of that user's events in [timestamp - T, timestamp] (before this one) is < N.
    """
    result = []
    # per user: list of timestamps we've already allowed (so we count them in the window)
    user_timestamps = {}

    for user_id, ts in events:
        low = ts - T
        # get this user's timestamps we've already allowed
        times = user_timestamps.get(user_id, [])
        # count how many of those fall in [low, ts] (inclusive)
        count_in_window = sum(1 for t in times if low <= t <= ts)
        if count_in_window < N:
            result.append("allowed")
            user_timestamps.setdefault(user_id, []).append(ts)
        else:
            result.append("rate_limited")

    return result


# ---------------------------------------------------------------------------
# Follow-ups (with clean commented examples)
# ---------------------------------------------------------------------------

def process_events_with_quota(events: list, N: int, T: int) -> list:
    """
    F1: Return list of (outcome, remaining_quota). remaining = N - count_after_this for allowed, else 0.
    Example:
        process_events_with_quota([("u1", 0), ("u1", 1), ("u1", 2)], 2, 5)
        -> [("allowed", 1), ("allowed", 0), ("rate_limited", 0)]
    """
    result = []
    user_timestamps = {}
    for user_id, ts in events:
        low = ts - T
        times = user_timestamps.get(user_id, [])
        count_in_window = sum(1 for t in times if low <= t <= ts)
        if count_in_window < N:
            result.append(("allowed", N - count_in_window - 1))
            user_timestamps.setdefault(user_id, []).append(ts)
        else:
            result.append(("rate_limited", 0))
    return result


def process_events_per_tier(events: list, get_limit, T: int) -> list:
    """
    F2: get_limit(user_id) returns N for that user. Same sliding-window logic, N per user.
    Example:
        get_limit = lambda u: 10 if u == "premium" else 2
        process_events_per_tier([("premium", 0), ("premium", 1), ("free", 0), ("free", 1), ("free", 2)], get_limit, 5)
        -> ["allowed", "allowed", "allowed", "allowed", "rate_limited"]
    """
    result = []
    user_timestamps = {}
    for user_id, ts in events:
        N = get_limit(user_id)
        low = ts - T
        times = user_timestamps.get(user_id, [])
        count_in_window = sum(1 for t in times if low <= t <= ts)
        if count_in_window < N:
            result.append("allowed")
            user_timestamps.setdefault(user_id, []).append(ts)
        else:
            result.append("rate_limited")
    return result


def run_tests():
    # Example: N=2, T=5. (u1,0) allowed; (u1,1) allowed; (u1,2) 2 already in window → rate_limited; (u2,3) allowed; (u1,6) only (u1,1) in [1,6] from allowed → allowed
    events = [("u1", 0), ("u1", 1), ("u1", 2), ("u2", 3), ("u1", 6)]
    assert process_events(events, N=2, T=5) == ["allowed", "allowed", "rate_limited", "allowed", "allowed"]

    # One user, N=1
    assert process_events([("a", 0), ("a", 0)], 1, 5) == ["allowed", "rate_limited"]

    # One user, N=2, T=0 → only same timestamp counts
    assert process_events([("a", 0), ("a", 0), ("a", 0)], 2, 0) == ["allowed", "allowed", "rate_limited"]

    # Two users independent
    assert process_events([("u1", 0), ("u2", 0), ("u1", 0)], 1, 10) == ["allowed", "allowed", "rate_limited"]

    # Follow-ups
    q = process_events_with_quota([("u1", 0), ("u1", 1), ("u1", 2)], 2, 5)
    assert q == [("allowed", 1), ("allowed", 0), ("rate_limited", 0)]
    get_limit = lambda u: 10 if u == "premium" else 2
    r = process_events_per_tier([("premium", 0), ("premium", 1), ("free", 0), ("free", 1), ("free", 2)], get_limit, 5)
    assert r == ["allowed", "allowed", "allowed", "allowed", "rate_limited"]

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
