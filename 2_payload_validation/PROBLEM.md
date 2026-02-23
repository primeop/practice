# Practice 2: API Payload Validation

**Why this:** Stripe deals with API payloads and webhooks; security engineers care about validation and safe handling of input.

## Problem

You receive a **payload** represented as a Python dict (as if from JSON). You need to validate it and extract a few fields safely.

Rules:

1. **`validate_charge_payload(payload: dict) -> tuple[bool, str]`**  
   - Returns `(True, "")` if valid.  
   - Returns `(False, "error message")` if invalid.  
   - **Valid** means:
     - Has key `"amount"` and it's an integer > 0.
     - Has key `"currency"` and it's a non-empty string of exactly 3 uppercase letters.
     - No other keys are required; extra keys are allowed.
   - Prefer one clear error message, e.g. "missing amount", "invalid currency", "amount must be positive".

2. **`get_amount_cents(payload: dict) -> int | None`**  
   Return the value of `"amount"` if the payload is valid (by the rules above); otherwise return `None`.  
   Reuse your validation logic.

**Edge cases:** `payload` is `None`, empty dict, wrong types (e.g. `amount` is string), currency not 3 chars or not uppercase.

Write manual tests that cover valid payload, missing fields, invalid types, and edge cases.

---

## Possible follow-ups (practice extending your solution)

- **F1 — Optional description:** Add optional field `"description"`: if present, must be a string with length ≤ 500. Otherwise valid. Return error `"description too long"` if longer.
- **F2 — Currency-specific rules:** Different currencies have different min/max amount. E.g. `USD` allows 1–99999999, `JPY` allows 1–999999 (no decimals). Add `validate_charge_payload(payload, currency_limits: dict)` and return error if amount out of range for that currency.
- **F3 — Return all errors:** Instead of first error only, add `validate_charge_payload_all_errors(payload) -> tuple[bool, list[str]]`. Collect all validation errors (e.g. `["missing amount", "invalid currency"]`) and return them together.
- **F4 — Nested metadata:** Allow optional key `"metadata"`. If present, it must be a dict with string keys and string values only; otherwise return `"invalid metadata"`.

**Implemented in solution.py:** `validate_charge_payload_with_description` (F1), `validate_charge_payload_all_errors` (F3). F2 (currency_limits) and F4 (metadata) are good extensions to try yourself.
