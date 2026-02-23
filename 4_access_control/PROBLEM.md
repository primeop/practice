# Practice 4: Access-Control System (Stripe-Style Interview)

**Format:** One main question + four follow-ups. Function-based (HackerRank-friendly). Based on real-world authorization at a company like Stripe, toned down. Focus on design, extension, filtering, and edge cases—not classic LeetCode.

---

## Question 1 (Main): Hierarchical Role-Based Access Control

Design a small **access-control system** with **hierarchical role inheritance**.

- **Roles** have **permissions**. Example roles: `"viewer"`, `"support"`, `"admin"`.
- **Hierarchy:** A role inherits all permissions from its parent(s). Example: `admin` → inherits from `support` → inherits from `viewer`. So if `viewer` has `read:charges`, then `support` and `admin` also have `read:charges` unless overridden.
- You are given:
  - **`role_permissions`**: `dict[str, list[str]]` — each role to list of permission strings (e.g. `"read:charges"`, `"write:customers"`).
  - **`role_hierarchy`**: `list[tuple[str, str]]` — list of `(child_role, parent_role)` meaning "child inherits from parent". Example: `[("admin", "support"), ("support", "viewer")]`.

Implement:

- **`has_permission(role: str, permission: str, role_permissions: dict, role_hierarchy: list) -> bool`**  
  Return `True` if the role (or any of its ancestors) has that permission; otherwise `False`.

**Edge cases to consider:** unknown role, unknown permission, empty hierarchy, role with no permissions, long inheritance chain.

---

## Follow-up 1: Filtering / Scoped Permissions

In practice, some permissions are **scoped**. For example, `support` might have `read:charges` only for a specific team: `team_id=team_123`.

- Extend the model so a permission can optionally have a **scope filter** (e.g. `{"team_id": "team_123"}`).
- **`has_permission(role, permission, scope, role_permissions, role_hierarchy)`**  
  If the role’s permission has a scope, then `scope` must be provided and must match (all filter keys present in `scope` and values equal). If the role’s permission has no scope, any `scope` is allowed.  
  You can represent permissions as `"permission_string"` (no filter) or `("permission_string", {"team_id": "team_123"})` or another clear format.

Implement this filtering logic without breaking the original behavior when no scope is used.

---

## Follow-up 2: Explicit Deny (Deny Overrides Allow)

Sometimes we need an **explicit deny**: e.g. `viewer` can have `read:refunds` denied even if an ancestor role allows it.

- Extend so that permissions can be **allow** or **deny** (e.g. `"allow:read:charges"` vs `"deny:read:refunds"`).
- Rule: **If any role in the inheritance chain has a deny for that permission, the result is False.** Otherwise, if any has allow, the result is True. No allow and no deny → False.

Update **`has_permission`** to support allow/deny and inheritance (including from parent roles).

---

## Follow-up 3: Effective Permissions (Flatten Inheritance)

Add a function that returns **all effective permissions** for a role (including inherited), in a form that’s easy to use elsewhere.

- **`get_effective_permissions(role: str, role_permissions: dict, role_hierarchy: list) -> set`**  
  Return the set of all permission strings this role effectively has (from itself and ancestors). You can start with the simple model (no scope, no deny) for this part, or extend to include scoped/allow-only if you prefer.

Handle **cycles** in the hierarchy (e.g. A → B → A): avoid infinite loops and define a sensible result (e.g. treat as no inheritance for the cycle, or raise).

---

## Follow-up 4: Edge Cases and Robustness

Discuss and implement handling for:

1. **Unknown role:** `has_permission("unknown_role", "read:charges", ...)` → return `False`, no crash.
2. **Empty hierarchy:** Role with no parents still has its own permissions.
3. **Cycle in hierarchy:** A → B → A. Ensure you don’t loop forever; e.g. collect roles visited and skip re-visiting, or raise a clear error.
4. **Empty or missing permissions:** Role not in `role_permissions` → treat as no permissions for that role (inheritance still applies).

Write tests that cover these edge cases.

---

## Possible additional follow-ups (beyond F1–F4 above)

- **F5 — Wildcard permissions:** Support permission strings like `"read:*"` meaning “all read actions.” For `has_permission(role, "read:charges", ...)`, return True if the role has either `"read:charges"` or `"read:*"`. Define matching rule clearly (e.g. `action:resource` vs `action:*`).
- **F6 — List permissions with filter:** `list_permissions_for_role(role, role_permissions, role_hierarchy, action_filter=None, resource_filter=None) -> set`. Return effective permissions, optionally filtered by prefix (e.g. only `read:*` or only `*:charges`). Reuse effective-permissions logic, then filter by string prefix.
- **F7 — Time-bound permissions (discuss only):** Permissions valid only within a time range. Discuss how you’d extend the data model (e.g. store valid_from/valid_until per permission) and how `has_permission` would change. No need to implement.

**Implemented in solution.py:** Main Q1 + F1–F4 are fully implemented. Additional: `has_permission_with_wildcard` (F5), `list_permissions_for_role(..., action_filter=..., resource_filter=...)` (F6). F7 is discussion-only.

---

## Realistic 45-min follow-ups (short extensions, often asked)

These are quick to add in the last 5–10 minutes of a 45-min slot; they reuse `has_permission` or `get_effective_permissions`.

- **F8 — Has all permissions:** `has_all_permissions(role: str, permissions: list[str], role_permissions: dict, role_hierarchy: list) -> bool`. Return `True` iff the role has **every** permission in the list (e.g. check before allowing a multi-step operation). Reuse `has_permission` in a loop.
- **F9 — Roles that have a permission:** `roles_with_permission(permission: str, role_permissions: dict, role_hierarchy: list) -> set[str]`. Return the set of **all role names** that (directly or via inheritance) have this permission. Useful for “who can do X?” or auditing. Collect all roles from `role_permissions` and hierarchy, then filter by `has_permission`.
- **F10 — Has any permission for an action:** `has_any_permission_with_action(role: str, action: str, role_permissions: dict, role_hierarchy: list) -> bool`. Return `True` if the role has **any** permission of the form `action:resource` (e.g. any `read:*`). Reuse `get_effective_permissions` and check if any perm starts with `action + ":"`.

**Implemented in solution.py:** `has_all_permissions` (F8), `roles_with_permission` (F9), `has_any_permission_with_action` (F10).
