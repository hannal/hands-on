ALLOWED_RESOURCES = {
    "role1": frozenset(("Query:/users",)),
    "role2": frozenset(("Query:/roles", "Query:/users/roles")),
}


def check_authorization(
    user_roles: frozenset[str] | set[str], resources: str, action: str, **kwargs
):
    perm = f"{action}:{resources}"
    return any(
        (
            True
            for _role in user_roles
            if perm in ALLOWED_RESOURCES.get(_role, frozenset())
        )
    )
