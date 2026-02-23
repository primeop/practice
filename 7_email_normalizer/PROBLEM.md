# Practice 7: Email Normalization & Deduplication

**Why this:** Common Stripe interview question — email normalization and deduplication. Tests string manipulation, validation, and attention to detail.

## Problem

Normalize email addresses and detect duplicates. Stripe-style rules:

**Normalization rules:**
1. Convert to lowercase
2. Remove dots (`.`) from the local part (before `@`)
3. Remove everything after `+` (including `+`) from the local part
4. Keep domain as-is (case-insensitive but preserve original)

**Examples:**
- `Test.Email+tag@Example.com` → `testemail@example.com`
- `user.name+filter@domain.com` → `username@domain.com`
- `user@domain.com` → `user@domain.com` (no change)

Implement:

1. **`normalize_email(email: str) -> str | None`**  
   Normalize email according to rules above. Return None if email is invalid (no `@`, empty local/domain).

2. **`count_unique_emails(emails: list[str]) -> int`**  
   Normalize all emails and return count of unique normalized addresses.

3. **`group_duplicates(emails: list[str]) -> dict[str, list[str]]`**  
   Return `{normalized_email: [original1, original2, ...]}` grouping duplicates together.

**Edge cases:** invalid emails, empty list, emails with multiple `@`, empty local/domain parts.

---

## Possible follow-ups (practice extending your solution)

- **F1 — Domain alias map:** Some domains are equivalent (e.g. `gmail.com` and `googlemail.com`). Add `normalize_email(email, domain_aliases: dict)`. If domain (after lowercase) is a key in `domain_aliases`, replace with the value before returning. E.g. `domain_aliases = {"googlemail.com": "gmail.com"}` so `user@googlemail.com` → `user@gmail.com`.
- **F2 — Canonical representative:** In `group_duplicates`, for each normalized email, return the “canonical” original (e.g. first occurrence in the list). Add `get_canonical_email_per_group(emails: list) -> dict[str, str]` returning `{normalized: canonical_original}`.
- **F3 — Basic format validation:** Before normalizing, reject clearly invalid formats. Add `is_valid_email_format(email: str) -> bool`: must have exactly one `@`, non-empty local and domain, no spaces, domain has at least one `.`. Call it from `normalize_email` and return None if invalid. Keep rules simple (no full regex).
- **F4 — Max length:** Reject emails that are too long after normalization. Add optional `max_length: int = 254`. If `len(normalized) > max_length`, return None (or skip in count_unique / group_duplicates).

**Implemented in solution.py:** `normalize_email_with_aliases(email, domain_aliases)` (F1), `get_canonical_email_per_group(emails)` (F2), `is_valid_email_format(email)` (F3). F4 (max length) is an optional extension.
