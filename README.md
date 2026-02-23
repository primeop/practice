# Stripe Technical Screen – Practice Problems

Use these to get ready for the **45-minute technical exercise** (practical coding, clean and testable code, edge cases).

## How to practice

1. **Time yourself** (e.g. 25–35 min per problem).
2. **Read the problem** in `PROBLEM.md`, ask yourself clarifying questions (as you would in the interview).
3. **Implement** in your preferred language in a new file (e.g. `my_solution.py`). Don’t peek at `solution.py` until you’re done or stuck.
4. **Add tests** and edge cases, then run and fix.
5. **Explain out loud** as you code (thought process, design choices).

## Problems

| # | Topic | Focus |
|---|--------|--------|
| 1 | [HTTP log parser](1_http_log_parser/PROBLEM.md) | HTTP request/response, parsing, counting, clean functions |
| 2 | [API payload validation](2_payload_validation/PROBLEM.md) | Input validation, types, security-minded handling of API input |
| 3 | [Rate limiter](3_rate_limiter/PROBLEM.md) | Sliding window, per-entity state, practical API behavior |
| 4 | [**Access control (interview-style)**](4_access_control/PROBLEM.md) | **One question + 4 follow-ups:** hierarchical roles, scoped permissions, deny overrides, effective perms, edge cases |
| 5 | [Transaction fee calculator](5_transaction_fee_calculator/PROBLEM.md) | CSV parsing, business logic, fee calculation, data aggregation |
| 6 | [Webhook signature validator](6_webhook_signature_validator/PROBLEM.md) | HMAC verification, timestamp validation, security-minded validation |
| 7 | [Email normalizer](7_email_normalizer/PROBLEM.md) | String manipulation, normalization rules, deduplication |

Each folder has:
- `PROBLEM.md` – problem statement, edge cases, and **possible follow-ups** (F1, F2, …) to practice extending your solution
- `solution.py` – reference solution with inline tests (run with `python3 solution.py`)

Create your own `my_solution.py` in each folder for practice (templates are not in this repo).

## Quick run (check solutions)

```bash
python3 1_http_log_parser/solution.py
python3 2_payload_validation/solution.py
python3 3_rate_limiter/solution.py
python3 4_access_control/solution.py
python3 5_transaction_fee_calculator/solution.py
python3 6_webhook_signature_validator/solution.py
python3 7_email_normalizer/solution.py
```

All should print `All tests passed.`
