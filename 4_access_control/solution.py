"""
Access-Control System: Hierarchical roles, filtering, deny overrides, effective permissions.
Function-based (Q1 + Follow-ups 1–4) — HackerRank-friendly.

  Q1: has_permission(role, permission, role_permissions, role_hierarchy)
  F1: has_permission_with_scope(..., scope=...)  # scoped permissions
  F2: has_permission_with_deny(...)              # deny overrides allow
  F3: get_effective_permissions(role, ...)        # flatten inheritance
  F4: edge cases (unknown role, empty hierarchy, cycle, missing perms)

Run: python3 solution.py
"""

from collections import deque


# ---------------------------------------------------------------------------
# Question 1 (Main): Hierarchical Role-Based Access Control
# ---------------------------------------------------------------------------
# Example (from problem):
#   Roles: "viewer", "support", "admin".
#   role_permissions = {"viewer": ["read:charges", "read:customers"],
#                       "support": ["read:refunds", "write:customers"],
#                       "admin": ["write:charges", "delete:customers"]}
#   role_hierarchy = [("admin", "support"), ("support", "viewer")]
#     => admin inherits support, support inherits viewer.
#   So admin has: admin's perms + support's + viewer's (e.g. read:charges from viewer).
#   has_permission("admin", "read:charges", ...) => True (via viewer).
# ---------------------------------------------------------------------------

def _build_parent_map(role_hierarchy: list) -> dict:
    """Build role -> list of direct parent roles. Example: ("support","viewer") => parent_map["support"] = ["viewer"]."""
    parent_map = {}
    for child, parent in role_hierarchy:
        parent_map.setdefault(child, []).append(parent)
    return parent_map


def _get_roles_with_inheritance(role: str, role_hierarchy: list) -> list:
    """Return [role] + all ancestors (BFS). Example: role=admin, hierarchy above => [admin, support, viewer]. Visited set prevents infinite loop on cycles."""
    parent_map = _build_parent_map(role_hierarchy)
    result = []
    visited = set()
    q = deque([role])
    while q:
        r = q.popleft()
        if r in visited:
            continue
        visited.add(r)
        result.append(r)
        for parent in parent_map.get(r, []):
            if parent not in visited:
                q.append(parent)
    return result


def has_permission(
    role: str,
    permission: str,
    role_permissions: dict,
    role_hierarchy: list,
) -> bool:
    """
    Q1: Return True if role (or any ancestor) has the permission.
    Example: has_permission("support", "read:charges", role_permissions, role_hierarchy) => True
    because support inherits viewer and viewer has "read:charges". Unknown role => False.
    """
    roles_to_check = _get_roles_with_inheritance(role, role_hierarchy)
    for r in roles_to_check:
        perms = role_permissions.get(r, [])
        for p in perms:
            if isinstance(p, str) and p == permission:
                return True
    return False


# ---------------------------------------------------------------------------
# Follow-up 1: Scoped permissions (filtering)
# ---------------------------------------------------------------------------
# Example:
#   role_permissions = {
#       "viewer": ["read:charges"],  # no scope, works for any team
#       "support": [("read:charges", {"team_id": "team_123"})]  # scoped to team_123
#   }
#   has_permission_with_scope("viewer", "read:charges", role_permissions, [], None) => True
#   has_permission_with_scope("support", "read:charges", role_permissions, [], {"team_id": "team_123"}) => True
#   has_permission_with_scope("support", "read:charges", role_permissions, [], {"team_id": "other"}) => False
#   has_permission_with_scope("support", "read:charges", role_permissions, [], None) => False (scope required)
# ---------------------------------------------------------------------------

def _permission_matches_scope(perm_entry, permission: str, scope: dict) -> bool:
    """
    perm_entry can be:
    - "read:charges" -> matches any scope for that permission
    - ("read:charges", {"team_id": "t1"}) -> permission must match and scope must match
    """
    if isinstance(perm_entry, str):
        return perm_entry == permission and (scope is None or scope == {})
    if isinstance(perm_entry, tuple):
        if len(perm_entry) == 1:
            return perm_entry[0] == permission
        if len(perm_entry) == 2:
            perm, required_scope = perm_entry[0], perm_entry[1]
            if perm != permission:
                return False
            if required_scope is None or required_scope == {}:
                return True
            if scope is None:
                return False
            for k, v in required_scope.items():
                if scope.get(k) != v:
                    return False
            return True
    return False


def has_permission_with_scope(
    role: str,
    permission: str,
    role_permissions: dict,
    role_hierarchy: list,
    scope: dict = None,
) -> bool:
    """
    F1: Like has_permission but if a role's permission has a scope filter,
    the provided scope must match (all keys in filter must be present and equal).
    """
    if scope is None:
        scope = {}
    roles_to_check = _get_roles_with_inheritance(role, role_hierarchy)
    for r in roles_to_check:
        perms = role_permissions.get(r, [])
        for p in perms:
            if isinstance(p, tuple) and len(p) >= 2 and p[0] == "deny":
                if p[1] == permission:
                    return False
                continue
            if _permission_matches_scope(p, permission, scope):
                return True
            if isinstance(p, str) and p == permission:
                return True
    return False


# ---------------------------------------------------------------------------
# Follow-up 2: Explicit deny (deny overrides allow)
# ---------------------------------------------------------------------------
# Example:
#   role_permissions = {
#       "viewer": ["read:charges", "read:refunds"],  # allows both
#       "support": [("deny", "read:refunds"), "write:customers"]  # denies read:refunds
#   }
#   role_hierarchy = [("support", "viewer")]  # support inherits viewer
#   has_permission_with_deny("viewer", "read:refunds", ...) => True (viewer allows it)
#   has_permission_with_deny("support", "read:refunds", ...) => False (support denies it, deny wins)
#   has_permission_with_deny("support", "read:charges", ...) => True (inherited from viewer, no deny)
# ---------------------------------------------------------------------------

def has_permission_with_deny(
    role: str,
    permission: str,
    role_permissions: dict,
    role_hierarchy: list,
) -> bool:
    """
    F2: Permissions can be ("allow", "read:charges") or ("deny", "read:refunds").
    Deny anywhere in the chain -> False. Else allow anywhere -> True.
    """
    roles_to_check = _get_roles_with_inheritance(role, role_hierarchy)
    seen_deny = False
    seen_allow = False
    for r in roles_to_check:
        perms = role_permissions.get(r, [])
        for p in perms:
            if isinstance(p, tuple):
                if len(p) >= 2 and p[0] == "deny" and p[1] == permission:
                    seen_deny = True
                if len(p) >= 2 and p[0] == "allow" and p[1] == permission:
                    seen_allow = True
                if len(p) == 1 and p[0] == permission:
                    seen_allow = True
            else:
                if p == permission:
                    seen_allow = True
    if seen_deny:
        return False
    return seen_allow


# ---------------------------------------------------------------------------
# Follow-up 3: Effective permissions (flatten inheritance)
# ---------------------------------------------------------------------------
# Example:
#   role_permissions = {
#       "viewer": ["read:charges", "read:customers"],
#       "support": ["read:refunds", "write:customers"],
#       "admin": ["write:charges", "delete:customers"]
#   }
#   role_hierarchy = [("admin", "support"), ("support", "viewer")]
#   get_effective_permissions("admin", role_permissions, role_hierarchy) =>
#     {"read:charges", "read:customers", "read:refunds", "write:customers", "write:charges", "delete:customers"}
#   (admin's perms + support's + viewer's, all flattened into one set)
# ---------------------------------------------------------------------------

def get_effective_permissions(
    role: str,
    role_permissions: dict,
    role_hierarchy: list,
) -> set:
    """
    F3: Return set of all permission strings this role has (self + ancestors).
    Simple model only: plain permission strings. Cycles avoided via visited set.
    """
    roles_to_check = _get_roles_with_inheritance(role, role_hierarchy)
    result = set()
    for r in roles_to_check:
        perms = role_permissions.get(r, [])
        for p in perms:
            if isinstance(p, tuple):
                if len(p) >= 2 and p[0] == "allow":
                    result.add(p[1])
                elif len(p) >= 1 and p[0] != "deny":
                    result.add(p[0] if ":" in str(p[0]) else p[0])
            else:
                result.add(p)
    return result


# ---------------------------------------------------------------------------
# Follow-up 4: Edge cases — integrated into helpers above.
# ---------------------------------------------------------------------------
# Examples:
#   1. Unknown role: has_permission("unknown_role", "read:charges", ...) => False (no crash)
#   2. Empty hierarchy: has_permission("viewer", "read:charges", role_permissions, []) => True
#      (role still has its own permissions even with no parents)
#   3. Cycle: role_hierarchy = [("a", "b"), ("b", "a")]
#      _get_roles_with_inheritance("a", ...) => ["a", "b"] (visited set prevents infinite loop)
#   4. Missing role in role_permissions:
#      has_permission("admin", "read:charges", {"viewer": ["read:charges"]}, [("admin", "viewer")])
#      => True (admin inherits from viewer, even though admin not in role_permissions dict)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Follow-ups F5–F6: Wildcard permissions, list with filter (with clean examples)
# ---------------------------------------------------------------------------
# F5 Example: role has "read:*" => has_permission_with_wildcard(role, "read:charges", ...) => True
# F6 Example: list_permissions_for_role("admin", ..., action_filter="read") => {"read:charges", "read:customers", "read:refunds"}
# ---------------------------------------------------------------------------


def _permission_matches_wildcard(has_perm: str, needed: str) -> bool:
    """True if has_perm grants needed. Exact match or has_perm is 'action:*' and needed starts with 'action:'."""
    if has_perm == needed:
        return True
    if has_perm.endswith(":*"):
        prefix = has_perm[:-2]  # e.g. "read" from "read:*"
        return needed.startswith(prefix + ":")
    return False


def has_permission_with_wildcard(role: str, permission: str, role_permissions: dict, role_hierarchy: list) -> bool:
    """
    F5: Support wildcard: "read:*" grants any "read:resource". "read:charges" matches "read:*" or "read:charges".
    Example:
        role_permissions = {"viewer": ["read:*"]}
        has_permission_with_wildcard("viewer", "read:charges", role_permissions, []) => True
        has_permission_with_wildcard("viewer", "write:charges", role_permissions, []) => False
    """
    roles_to_check = _get_roles_with_inheritance(role, role_hierarchy)
    for r in roles_to_check:
        perms = role_permissions.get(r, [])
        for p in perms:
            if isinstance(p, str) and _permission_matches_wildcard(p, permission):
                return True
    return False


def list_permissions_for_role(role: str, role_permissions: dict, role_hierarchy: list,
                              action_filter: str = None, resource_filter: str = None) -> set:
    """
    F6: Return effective permissions (plain strings only), optionally filtered by action or resource prefix.
    Example:
        list_permissions_for_role("admin", role_permissions, role_hierarchy) => full set
        list_permissions_for_role("admin", role_permissions, role_hierarchy, action_filter="read") => {"read:charges", "read:customers", "read:refunds"}
        list_permissions_for_role("admin", role_permissions, role_hierarchy, resource_filter="charges") => {"read:charges", "write:charges"}
    """
    effective = get_effective_permissions(role, role_permissions, role_hierarchy)
    out = set()
    for perm in effective:
        if ":" not in perm:
            continue
        action, resource = perm.split(":", 1)
        if action_filter is not None and action != action_filter:
            continue
        if resource_filter is not None and resource != resource_filter:
            continue
        out.add(perm)
    return out


# ---------------------------------------------------------------------------
# Realistic 45-min follow-ups (F8–F10): short extensions, reuse existing logic
# ---------------------------------------------------------------------------
# F8 Example: has_all_permissions("admin", ["read:charges", "write:charges"], ...) => True
# F9 Example: roles_with_permission("read:charges", ...) => {"viewer", "support", "admin"}
# F10 Example: has_any_permission_with_action("support", "read", ...) => True (has read:charges, read:refunds, etc.)
# ---------------------------------------------------------------------------


def has_all_permissions(role: str, permissions: list, role_permissions: dict, role_hierarchy: list) -> bool:
    """
    F8: Return True iff role has every permission in the list. Reuse has_permission.
    Example: has_all_permissions("admin", ["read:charges", "write:charges"], rp, rh) => True
    """
    for perm in permissions:
        if not has_permission(role, perm, role_permissions, role_hierarchy):
            return False
    return True


def _all_roles(role_permissions: dict, role_hierarchy: list) -> set:
    """Collect all role names that appear in role_permissions or in hierarchy."""
    roles = set(role_permissions.keys())
    for child, parent in role_hierarchy:
        roles.add(child)
        roles.add(parent)
    return roles


def roles_with_permission(permission: str, role_permissions: dict, role_hierarchy: list) -> set:
    """
    F9: Return set of all role names that have this permission (directly or inherited).
    Example: roles_with_permission("read:charges", rp, rh) => {"viewer", "support", "admin"}
    """
    all_roles = _all_roles(role_permissions, role_hierarchy)
    return {r for r in all_roles if has_permission(r, permission, role_permissions, role_hierarchy)}


def has_any_permission_with_action(role: str, action: str, role_permissions: dict, role_hierarchy: list) -> bool:
    """
    F10: Return True if role has any permission of form "action:resource" (e.g. any read).
    Example: has_any_permission_with_action("support", "read", rp, rh) => True
    """
    prefix = action + ":"
    effective = get_effective_permissions(role, role_permissions, role_hierarchy)
    return any(p.startswith(prefix) for p in effective if isinstance(p, str) and ":" in p)


def run_tests():
    # ----- Q1: Basic hierarchy -----
    role_permissions = {
        "viewer": ["read:charges", "read:customers"],
        "support": ["read:refunds", "write:customers"],
        "admin": ["write:charges", "delete:customers"],
    }
    role_hierarchy = [("admin", "support"), ("support", "viewer")]

    assert has_permission("viewer", "read:charges", role_permissions, role_hierarchy) is True
    assert has_permission("viewer", "read:refunds", role_permissions, role_hierarchy) is False
    assert has_permission("support", "read:charges", role_permissions, role_hierarchy) is True
    assert has_permission("support", "read:refunds", role_permissions, role_hierarchy) is True
    assert has_permission("admin", "read:charges", role_permissions, role_hierarchy) is True
    assert has_permission("admin", "delete:customers", role_permissions, role_hierarchy) is True

    # Unknown role
    assert has_permission("unknown", "read:charges", role_permissions, role_hierarchy) is False
    # Empty hierarchy
    assert has_permission("viewer", "read:charges", role_permissions, []) is True

    # ----- F1: Scoped permissions -----
    role_permissions_scoped = {
        "viewer": ["read:charges"],
        "support": [("read:charges", {"team_id": "team_123"})],
    }
    assert has_permission_with_scope("viewer", "read:charges", role_permissions_scoped, [], None) is True
    assert has_permission_with_scope("support", "read:charges", role_permissions_scoped, [], {"team_id": "team_123"}) is True
    assert has_permission_with_scope("support", "read:charges", role_permissions_scoped, [], {"team_id": "other"}) is False
    assert has_permission_with_scope("support", "read:charges", role_permissions_scoped, [], None) is False

    # ----- F2: Deny overrides -----
    role_permissions_deny = {
        "viewer": ["read:charges", "read:refunds"],
        "support": [("deny", "read:refunds"), "write:customers"],
    }
    role_hierarchy_2 = [("support", "viewer")]
    assert has_permission_with_deny("viewer", "read:refunds", role_permissions_deny, role_hierarchy_2) is True
    assert has_permission_with_deny("support", "read:refunds", role_permissions_deny, role_hierarchy_2) is False
    assert has_permission_with_deny("support", "read:charges", role_permissions_deny, role_hierarchy_2) is True

    # ----- F3: Effective permissions -----
    effective = get_effective_permissions("admin", role_permissions, role_hierarchy)
    expected = {"read:charges", "read:customers", "read:refunds", "write:customers", "write:charges", "delete:customers"}
    assert effective == expected
    assert get_effective_permissions("unknown", role_permissions, role_hierarchy) == set()

    # ----- F4: Cycle -----
    cycle_hierarchy = [("a", "b"), ("b", "a")]
    roles_with_cycle = _get_roles_with_inheritance("a", cycle_hierarchy)
    assert "a" in roles_with_cycle and "b" in roles_with_cycle
    assert len(roles_with_cycle) == 2  # no infinite loop

    # Role not in role_permissions
    assert has_permission("admin", "read:charges", {"viewer": ["read:charges"]}, [("admin", "viewer")]) is True

    # ----- F5: Wildcard -----
    rp_wild = {"viewer": ["read:*"]}
    assert has_permission_with_wildcard("viewer", "read:charges", rp_wild, []) is True
    assert has_permission_with_wildcard("viewer", "write:charges", rp_wild, []) is False

    # ----- F6: List with filter -----
    listed = list_permissions_for_role("admin", role_permissions, role_hierarchy, action_filter="read")
    assert listed == {"read:charges", "read:customers", "read:refunds"}
    listed2 = list_permissions_for_role("admin", role_permissions, role_hierarchy, resource_filter="charges")
    assert "read:charges" in listed2 and "write:charges" in listed2

    # ----- F8: Has all permissions -----
    assert has_all_permissions("admin", ["read:charges", "write:charges"], role_permissions, role_hierarchy) is True
    assert has_all_permissions("viewer", ["read:charges", "write:charges"], role_permissions, role_hierarchy) is False

    # ----- F9: Roles with permission -----
    rwp = roles_with_permission("read:charges", role_permissions, role_hierarchy)
    assert rwp == {"viewer", "support", "admin"}
    assert roles_with_permission("delete:customers", role_permissions, role_hierarchy) == {"admin"}

    # ----- F10: Has any permission with action -----
    assert has_any_permission_with_action("support", "read", role_permissions, role_hierarchy) is True
    assert has_any_permission_with_action("viewer", "write", role_permissions, role_hierarchy) is False

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
