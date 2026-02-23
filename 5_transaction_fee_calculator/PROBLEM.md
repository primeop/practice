# Practice 5: Transaction Fee Calculator (CSV Parsing)

**Why this:** Common Stripe interview question — parsing CSV transaction records, calculating fees based on status, aggregating by user. Tests CSV parsing, business logic, and data aggregation.

## Problem

You're given a CSV file (as a list of strings) representing transactions. Each line has:
```
user_id,amount,status
```

Example:
```
user123,1000,completed
user123,500,failed
user456,2000,completed
user123,300,completed
```

**Fee rules:**
- `completed` transactions: fee = 2% of amount (rounded down)
- `failed` transactions: fee = 0
- `pending` transactions: fee = 0 (not charged yet)

Implement:

1. **`parse_transaction(line: str) -> dict | None`**  
   Parse one CSV line and return `{"user_id": str, "amount": int, "status": str}`.  
   Return `None` if line is invalid (wrong format, non-numeric amount, empty fields).

2. **`calculate_fee(amount: int, status: str) -> int`**  
   Return the fee in cents based on the rules above.

3. **`calculate_user_fees(transactions: list[str]) -> dict[str, int]`**  
   Parse all transactions, calculate fees, and return `{user_id: total_fee}`.  
   Skip invalid lines (return None from parse_transaction).

**Edge cases:** empty list, invalid CSV lines, missing fields, negative amounts, unknown status.

Write tests covering valid transactions, invalid lines, and edge cases.

---

## Possible follow-ups (practice extending your solution)

- **F1 — New status with different fee:** Add status `"dispute_won"`: fee = 15 (fixed) if provider is `"card"`, else 0. Transactions now have 4 fields: `user_id,amount,status,provider`. Add `calculate_fee(amount, status, provider)` and update aggregation. Keep backward compatibility for lines without provider (e.g. default provider).
- **F2 — Variable rate by provider:** For `completed`, fee = amount × rate(provider) (rounded down). E.g. `rate_map = {"card": 0.02, "paypal": 0.03}`. Add `calculate_user_fees(transactions, rate_map)` and use a default rate (e.g. 0.02) if provider not in map.
- **F3 — Aggregate by (user, month):** Assume each transaction line has optional 5th field `timestamp` (e.g. Unix seconds). Add `calculate_user_fees_by_month(transactions) -> dict[tuple[str, str], int]` returning `{(user_id, "YYYY-MM"): total_fee}`. Ignore transactions without timestamp or use “unknown” month.
- **F4 — Report invalid lines:** Add `calculate_user_fees_with_errors(transactions) -> tuple[dict[str, int], int]`. Return `(user_fees_dict, invalid_line_count)`. Same logic as before but also count how many lines were skipped as invalid.

**Implemented in solution.py:** `parse_transaction_with_provider` (for F1/F2), `calculate_fee_with_provider` (F1), `calculate_user_fees_with_rates` (F2), `calculate_user_fees_with_errors` (F4). F3 (by month) is an optional extension.
