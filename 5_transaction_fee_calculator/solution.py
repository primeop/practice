"""
Transaction Fee Calculator - Solution with manual tests.
Run: python3 solution.py
"""


def parse_transaction(line: str):
    """Parse CSV line: user_id,amount,status. Return dict or None if invalid."""
    line = line.strip()
    if not line:
        return None
    parts = line.split(",")
    if len(parts) != 3:
        return None
    user_id, amount_str, status = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if not user_id or not amount_str or not status:
        return None
    if not amount_str.isdigit():
        return None
    amount = int(amount_str)
    if amount < 0:
        return None
    return {"user_id": user_id, "amount": amount, "status": status}


def calculate_fee(amount: int, status: str) -> int:
    """Calculate fee: completed = 2% (rounded down), failed/pending = 0."""
    if status == "completed":
        return int(amount * 0.02)  # 2%, rounded down
    return 0


def calculate_user_fees(transactions: list) -> dict:
    """Parse transactions, calculate fees per user. Skip invalid lines."""
    user_fees = {}
    for line in transactions:
        txn = parse_transaction(line)
        if txn is None:
            continue
        user_id = txn["user_id"]
        fee = calculate_fee(txn["amount"], txn["status"])
        user_fees[user_id] = user_fees.get(user_id, 0) + fee
    return user_fees


# ---------------------------------------------------------------------------
# Follow-ups (with clean commented examples)
# ---------------------------------------------------------------------------

def parse_transaction_with_provider(line: str):
    """Parse CSV: user_id,amount,status,provider (provider optional). Return dict or None."""
    line = line.strip()
    if not line:
        return None
    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 3:
        return None
    user_id, amount_str, status = parts[0], parts[1], parts[2]
    provider = parts[3] if len(parts) > 3 else "card"
    if not user_id or not amount_str or not status:
        return None
    if not amount_str.isdigit():
        return None
    amount = int(amount_str)
    if amount < 0:
        return None
    return {"user_id": user_id, "amount": amount, "status": status, "provider": provider}


def calculate_fee_with_provider(amount: int, status: str, provider: str = "card") -> int:
    """
    F1: completed = 2% (rounded down); dispute_won = 15 if provider == 'card' else 0; failed/pending = 0.
    Example:
        calculate_fee_with_provider(1000, "completed", "card") -> 20
        calculate_fee_with_provider(0, "dispute_won", "card") -> 15
        calculate_fee_with_provider(0, "dispute_won", "paypal") -> 0
    """
    if status == "completed":
        return int(amount * 0.02)
    if status == "dispute_won":
        return 15 if provider == "card" else 0
    return 0


def calculate_user_fees_with_rates(transactions: list, rate_map: dict) -> dict:
    """
    F2: completed fee = amount * rate_map.get(provider, 0.02). CSV format: user_id,amount,status,provider.
    Example:
        rate_map = {"card": 0.02, "paypal": 0.03}
        transactions = ["u1,1000,completed,card", "u1,1000,completed,paypal"]
        calculate_user_fees_with_rates(transactions, rate_map) -> {"u1": 50}  # 20 + 30
    """
    user_fees = {}
    for line in transactions:
        txn = parse_transaction_with_provider(line)
        if txn is None:
            continue
        if txn["status"] != "completed":
            continue
        rate = rate_map.get(txn["provider"], 0.02)
        fee = int(txn["amount"] * rate)
        user_id = txn["user_id"]
        user_fees[user_id] = user_fees.get(user_id, 0) + fee
    return user_fees


def calculate_user_fees_with_errors(transactions: list) -> tuple:
    """
    F4: Return (user_fees_dict, invalid_line_count). Same logic as calculate_user_fees but count skipped lines.
    Example:
        calculate_user_fees_with_errors(["u1,1000,completed", "bad", "u1,500,failed"]) -> ({"u1": 20}, 1)
    """
    user_fees = {}
    invalid_count = 0
    for line in transactions:
        txn = parse_transaction(line)
        if txn is None:
            invalid_count += 1
            continue
        user_id = txn["user_id"]
        fee = calculate_fee(txn["amount"], txn["status"])
        user_fees[user_id] = user_fees.get(user_id, 0) + fee
    return user_fees, invalid_count


def run_tests():
    transactions = [
        "user123,1000,completed",
        "user123,500,failed",
        "user456,2000,completed",
        "user123,300,completed",
    ]
    
    # parse_transaction
    assert parse_transaction("user123,1000,completed") == {"user_id": "user123", "amount": 1000, "status": "completed"}
    assert parse_transaction("") is None
    assert parse_transaction("user123,1000") is None
    assert parse_transaction("user123,abc,completed") is None
    
    # calculate_fee
    assert calculate_fee(1000, "completed") == 20  # 2% of 1000
    assert calculate_fee(500, "failed") == 0
    assert calculate_fee(300, "pending") == 0
    
    # calculate_user_fees
    result = calculate_user_fees(transactions)
    assert result["user123"] == 26  # 20 + 0 + 6 = 26
    assert result["user456"] == 40  # 2% of 2000

    # Follow-ups
    assert calculate_fee_with_provider(1000, "completed", "card") == 20
    assert calculate_fee_with_provider(0, "dispute_won", "card") == 15
    assert calculate_fee_with_provider(0, "dispute_won", "paypal") == 0
    r = calculate_user_fees_with_rates(["u1,1000,completed,card", "u1,1000,completed,paypal"], {"card": 0.02, "paypal": 0.03})
    assert r["u1"] == 50
    fees, inv = calculate_user_fees_with_errors(["u1,1000,completed", "bad", "u1,500,failed"])
    assert fees == {"u1": 20} and inv == 1

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
