"""
Webhook Signature Validator - Solution with manual tests.
Run: python3 solution.py
"""
import hmac
import hashlib
import time


def parse_signature_header(header: str):
    """Parse Stripe-Signature header: t=timestamp,v1=sig1,v0=sig0. Return dict or None."""
    if not header:
        return None
    result = {}
    parts = header.split(",")
    for part in parts:
        part = part.strip()
        if "=" not in part:
            return None
        key, value = part.split("=", 1)
        result[key] = value
    if "t" not in result or "v1" not in result:
        return None
    return {"t": result["t"], "v1": result["v1"]}


def verify_timestamp(timestamp_str: str, max_age_seconds: int = 300) -> tuple:
    """Check if timestamp is valid and recent. Return (True, "") or (False, "error message")."""
    try:
        timestamp = int(timestamp_str)
    except ValueError:
        return False, "invalid timestamp format"
    current_time = int(time.time())
    age = current_time - timestamp
    if age < 0:
        return False, "timestamp is in the future"
    if age > max_age_seconds:
        return False, f"timestamp too old (age: {age}s, max: {max_age_seconds}s)"
    return True, ""


def verify_webhook_signature(timestamp: str, body: str, signature: str, secret: str) -> bool:
    """Compute HMAC-SHA256(timestamp + "." + body, secret) and compare to signature."""
    payload = f"{timestamp}.{body}"
    expected = hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


# ---------------------------------------------------------------------------
# Follow-ups (with clean commented examples)
# ---------------------------------------------------------------------------

def verify_webhook_full(header: str, body: str, secret: str, max_age_seconds: int = 300) -> tuple:
    """
    F2: Return (True, "") if valid; else (False, reason).
    Reason: "missing_header", "invalid_header", "timestamp_too_old", "invalid_signature".
    Example:
        verify_webhook_full("t=...,v1=...", body, secret) -> (True, "") or (False, "invalid_signature")
        verify_webhook_full("", body, secret) -> (False, "missing_header")
    """
    if not header:
        return False, "missing_header"
    parsed = parse_signature_header(header)
    if parsed is None:
        return False, "invalid_header"
    ts, sig = parsed["t"], parsed["v1"]
    ok_ts, msg_ts = verify_timestamp(ts, max_age_seconds)
    if not ok_ts:
        return False, "timestamp_too_old"
    if not verify_webhook_signature(ts, body, sig, secret):
        return False, "invalid_signature"
    return True, ""


def verify_webhook_and_event_type(body_json: dict, allowed_types: set) -> tuple:
    """
    F3: Assume signature already verified. Check body_json["type"] is in allowed_types.
    Return (True, "") or (False, "event_type_not_allowed").
    Example:
        verify_webhook_and_event_type({"type": "charge.succeeded"}, {"charge.succeeded"}) -> (True, "")
        verify_webhook_and_event_type({"type": "charge.failed"}, {"charge.succeeded"}) -> (False, "event_type_not_allowed")
    """
    event_type = body_json.get("type")
    if event_type not in allowed_types:
        return False, "event_type_not_allowed"
    return True, ""


def run_tests():
    # parse_signature_header
    header = "t=1234567890,v1=abc123,v0=old123"
    parsed = parse_signature_header(header)
    assert parsed == {"t": "1234567890", "v1": "abc123"}
    assert parse_signature_header("") is None
    assert parse_signature_header("invalid") is None
    
    # verify_timestamp
    current = str(int(time.time()))
    assert verify_timestamp(current)[0] is True
    old = str(int(time.time()) - 400)
    assert verify_timestamp(old)[0] is False
    
    # verify_webhook_signature
    secret = "whsec_test123"
    timestamp = "1234567890"
    body = '{"type":"charge.succeeded","id":"evt_123"}'
    # Note: In real interview, you'd compute this or be given test cases

    # Follow-ups
    ok, reason = verify_webhook_full("", body, secret)
    assert ok is False and reason == "missing_header"
    ok2, reason2 = verify_webhook_and_event_type({"type": "charge.succeeded"}, {"charge.succeeded", "charge.failed"})
    assert ok2 is True
    ok3, reason3 = verify_webhook_and_event_type({"type": "unknown"}, {"charge.succeeded"})
    assert ok3 is False and reason3 == "event_type_not_allowed"

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
