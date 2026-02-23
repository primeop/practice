"""
Email Normalization & Deduplication - Solution with manual tests.
Run: python3 solution.py
"""


def normalize_email(email: str):
    """Normalize email: lowercase, remove dots and +tag from local part."""
    if not email or "@" not in email:
        return None
    parts = email.split("@", 1)
    if len(parts) != 2:
        return None
    local, domain = parts[0], parts[1]
    if not local or not domain:
        return None
    # Remove dots and +tag from local part
    local = local.replace(".", "")
    if "+" in local:
        local = local.split("+")[0]
    # Lowercase both parts
    return f"{local.lower()}@{domain.lower()}"


def count_unique_emails(emails: list) -> int:
    """Count unique normalized emails."""
    normalized = set()
    for email in emails:
        norm = normalize_email(email)
        if norm:
            normalized.add(norm)
    return len(normalized)


def group_duplicates(emails: list) -> dict:
    """Group emails by normalized form."""
    groups = {}
    for email in emails:
        norm = normalize_email(email)
        if norm:
            groups.setdefault(norm, []).append(email)
    return groups


# ---------------------------------------------------------------------------
# Follow-ups (with clean commented examples)
# ---------------------------------------------------------------------------

def normalize_email_with_aliases(email: str, domain_aliases: dict = None) -> str:
    """
    F1: Normalize email; if domain_aliases maps domain -> canonical, replace domain first.
    Example:
        normalize_email_with_aliases("user@googlemail.com", {"googlemail.com": "gmail.com"}) -> "user@gmail.com"
        normalize_email_with_aliases("user@gmail.com", {"googlemail.com": "gmail.com"}) -> "user@gmail.com"
    """
    norm = normalize_email(email)
    if norm is None:
        return None
    if not domain_aliases:
        return norm
    local, domain = norm.split("@", 1)
    domain = domain_aliases.get(domain, domain)
    return f"{local}@{domain}"


def get_canonical_email_per_group(emails: list) -> dict:
    """
    F2: Return {normalized: canonical_original} where canonical is first occurrence in list.
    Example:
        get_canonical_email_per_group(["test.email@ex.com", "testemail@ex.com", "other@ex.com"])
        -> {"testemail@ex.com": "test.email@ex.com", "other@ex.com": "other@ex.com"}
    """
    result = {}
    for email in emails:
        norm = normalize_email(email)
        if norm and norm not in result:
            result[norm] = email
    return result


def is_valid_email_format(email: str) -> bool:
    """
    F3: Basic format: exactly one @, non-empty local and domain, no spaces, domain has at least one '.'.
    Example:
        is_valid_email_format("a@b.c") -> True
        is_valid_email_format("invalid") -> False
        is_valid_email_format("a @b.c") -> False
    """
    if not email or " " in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    local, domain = parts[0], parts[1]
    if not local or not domain:
        return False
    if "." not in domain:
        return False
    return True


def run_tests():
    # normalize_email
    assert normalize_email("Test.Email+tag@Example.com") == "testemail@example.com"
    assert normalize_email("user.name+filter@domain.com") == "username@domain.com"
    assert normalize_email("user@domain.com") == "user@domain.com"
    assert normalize_email("invalid") is None
    assert normalize_email("@domain.com") is None
    
    # count_unique_emails
    emails = [
        "test.email+tag@example.com",
        "testemail@example.com",
        "user@domain.com",
        "user.name@domain.com",
    ]
    assert count_unique_emails(emails) == 3  # testemail@example.com, user@domain.com, username@domain.com
    
    # group_duplicates
    groups = group_duplicates(emails)
    assert "testemail@example.com" in groups
    assert len(groups["testemail@example.com"]) == 2

    # Follow-ups
    assert normalize_email_with_aliases("user@googlemail.com", {"googlemail.com": "gmail.com"}) == "user@gmail.com"
    canon = get_canonical_email_per_group(["test.email@ex.com", "testemail@ex.com"])
    assert canon["testemail@ex.com"] == "test.email@ex.com"
    assert is_valid_email_format("a@b.c") is True
    assert is_valid_email_format("invalid") is False
    assert is_valid_email_format("a @b.c") is False

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
