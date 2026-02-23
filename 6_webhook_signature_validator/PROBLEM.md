# Practice 6: Webhook Signature Validator

**Why this:** Stripe uses webhook signature verification for security. This tests string manipulation, HMAC understanding, and security-minded validation.

## Problem

Stripe webhooks include a `Stripe-Signature` header with format:
```
t=timestamp,v1=signature1,v0=signature0
```

The signature is computed as: `HMAC-SHA256(timestamp + "." + body, secret)`

**Rules:**
- Verify the signature matches the expected value
- Check timestamp is recent (within last 5 minutes) to prevent replay attacks
- Return clear error messages

Implement:

1. **`parse_signature_header(header: str) -> dict | None`**  
   Parse the header and return `{"t": timestamp_str, "v1": signature_str}` or None if invalid format.

2. **`verify_timestamp(timestamp_str: str, max_age_seconds: int = 300) -> tuple[bool, str]`**  
   Return `(True, "")` if timestamp is valid and recent, else `(False, "error message")`.

3. **`verify_webhook_signature(timestamp: str, body: str, signature: str, secret: str) -> bool`**  
   Compute HMAC-SHA256 of `timestamp + "." + body` with secret, compare to signature.  
   Return True if match, False otherwise.

**Note:** For the interview, you might be asked to implement the HMAC logic or use a library. Clarify if you can use `hmac` module.

**Edge cases:** missing header, malformed header, old timestamp, wrong signature.

---

## Possible follow-ups (practice extending your solution)

- **F1 — Try v0 and v1:** Stripe sends both `v0` and `v1` in the header. Add `verify_webhook_signature_v0_or_v1(timestamp, body, header, secret) -> bool`. Parse header for both `v0` and `v1`; compute expected for both; return True if either matches (allows key rotation).
- **F2 — Specific error reason:** Instead of just True/False, add `verify_webhook_full(header, body, secret, max_age_seconds=300) -> tuple[bool, str]`. Return `(True, "")` if valid; else `(False, "missing_header"|"invalid_header"|"timestamp_too_old"|"invalid_signature")` so callers can log or handle differently.
- **F3 — Allowed event types:** After signature verification, validate event type. Payload is JSON with `"type"` field (e.g. `"charge.succeeded"`). Add `verify_webhook_and_event_type(body_json: dict, allowed_types: set[str]) -> tuple[bool, str]`. Return `(False, "event_type_not_allowed")` if `body_json.get("type")` not in `allowed_types`; else `(True, "")`. Assume signature already verified.
- **F4 — Replay set:** To prevent replay, maintain a set of processed `(timestamp, signature)` or event IDs. Add `is_replay(timestamp: str, signature: str, seen: set) -> bool` and update `seen` when an event is accepted. Discuss how you’d do this in production (TTL, bounded set).

**Implemented in solution.py:** `verify_webhook_full(header, body, secret, max_age_seconds)` (F2) returns `(bool, "missing_header"|"invalid_header"|"timestamp_too_old"|"invalid_signature")`; `verify_webhook_and_event_type(body_json, allowed_types)` (F3). F1 (v0 or v1) and F4 (replay) are optional.
