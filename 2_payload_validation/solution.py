"""
API Payload Validation - Solution with manual tests.
Run: python solution.py
"""


def validate_charge_payload(payload: dict) -> tuple[bool, str]:
    """Returns (True, "") if valid, else (False, error_message)."""
    if payload is None:
        return False, "payload is required"
    if not isinstance(payload, dict):
        return False, "payload must be a dict"

    if "amount" not in payload:
        return False, "missing amount"
    amount = payload["amount"]
    if not isinstance(amount, int):
        return False, "amount must be an integer"
    if amount <= 0:
        return False, "amount must be positive"

    if "currency" not in payload:
        return False, "missing currency"
    currency = payload["currency"]
    if not isinstance(currency, str):
        return False, "currency must be a string"
    if len(currency) != 3 or currency != currency.upper():
        return False, "invalid currency"

    return True, ""


def get_amount_cents(payload: dict):
    """Return amount if payload is valid, else None."""
    ok, _ = validate_charge_payload(payload)
    if not ok:
        return None
    return payload["amount"]


# ---------------------------------------------------------------------------
# Follow-ups (with clean commented examples)
# ---------------------------------------------------------------------------

def validate_charge_payload_with_description(payload: dict, max_description_length: int = 500) -> tuple:
    """
    F1: Same as validate_charge_payload; if 'description' present, must be str with len <= max.
    Example:
        validate_charge_payload_with_description({"amount": 1000, "currency": "USD"}) -> (True, "")
        validate_charge_payload_with_description({"amount": 1000, "currency": "USD", "description": "short"}) -> (True, "")
        validate_charge_payload_with_description({"amount": 1000, "currency": "USD", "description": "x" * 501}) -> (False, "description too long")
    """
    ok, msg = validate_charge_payload(payload)
    if not ok:
        return ok, msg
    if "description" in payload:
        d = payload["description"]
        if not isinstance(d, str):
            return False, "description must be a string"
        if len(d) > max_description_length:
            return False, "description too long"
    return True, ""


def validate_charge_payload_all_errors(payload: dict) -> tuple:
    """
    F3: Return (True, []) if valid, else (False, list of all error strings).
    Example:
        validate_charge_payload_all_errors({}) -> (False, ["missing amount", "missing currency"])
        validate_charge_payload_all_errors({"amount": -1, "currency": "usd"}) -> (False, ["amount must be positive", "invalid currency"])
    """
    errors = []
    if payload is None:
        return False, ["payload is required"]
    if not isinstance(payload, dict):
        return False, ["payload must be a dict"]
    if "amount" not in payload:
        errors.append("missing amount")
    else:
        a = payload["amount"]
        if not isinstance(a, int):
            errors.append("amount must be an integer")
        elif a <= 0:
            errors.append("amount must be positive")
    if "currency" not in payload:
        errors.append("missing currency")
    else:
        c = payload["currency"]
        if not isinstance(c, str):
            errors.append("currency must be a string")
        elif len(c) != 3 or c != c.upper():
            errors.append("invalid currency")
    if errors:
        return False, errors
    return True, []


def run_tests():
    # Valid
    assert validate_charge_payload({"amount": 1000, "currency": "USD"}) == (True, "")
    assert validate_charge_payload({"amount": 1, "currency": "EUR", "id": "ch_123"}) == (True, "")

    # Missing / invalid amount
    assert validate_charge_payload({})[0] is False
    assert "amount" in validate_charge_payload({"currency": "USD"})[1].lower()
    assert validate_charge_payload({"amount": 0, "currency": "USD"})[0] is False
    assert validate_charge_payload({"amount": -1, "currency": "USD"})[0] is False
    assert validate_charge_payload({"amount": "1000", "currency": "USD"})[0] is False

    # Missing / invalid currency
    assert "currency" in validate_charge_payload({"amount": 1000})[1].lower()
    assert validate_charge_payload({"amount": 1000, "currency": "usd"})[0] is False
    assert validate_charge_payload({"amount": 1000, "currency": "US"})[0] is False

    # Edge cases
    assert validate_charge_payload(None)[0] is False

    # get_amount_cents
    assert get_amount_cents({"amount": 1000, "currency": "USD"}) == 1000
    assert get_amount_cents({"amount": 500, "currency": "GBP"}) == 500
    assert get_amount_cents({}) is None
    assert get_amount_cents(None) is None

    # Follow-ups
    assert validate_charge_payload_with_description({"amount": 1000, "currency": "USD"}) == (True, "")
    assert validate_charge_payload_with_description({"amount": 1000, "currency": "USD", "description": "ok"}) == (True, "")
    assert validate_charge_payload_with_description({"amount": 1000, "currency": "USD", "description": "x" * 501})[0] is False
    err_all = validate_charge_payload_all_errors({})
    assert err_all[0] is False and "amount" in str(err_all[1]).lower() and "currency" in str(err_all[1]).lower()

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
