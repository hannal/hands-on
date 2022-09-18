import typing as t

from strawberry.permission import BasePermission
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.types import Info
from strawberry.types.nodes import Selection
from graphql.pyutils.path import Path

from fastapi_authz.auth import BaseUser


def build_schema_keys(path: Path, keys: list):
    if path.typename:
        keys.append(path.key)
    if path.prev:
        return build_schema_keys(path.prev, keys)
    key_path = "/".join(keys[::-1])
    return f"/{key_path}", path.typename


def build_role_payload(
    user: BaseUser,
    path: Path,
    selected_fields: list[Selection],
):
    paths, schema_type = build_schema_keys(path, [])
    return {
        "user_roles": user.roles,
        "paths": paths,
        "type": schema_type,
    }


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: t.Any, info: Info, **kwargs) -> bool:
        user: BaseUser = info.context["user"]
        return user.is_authenticated


class HasRoles(BasePermission):
    message = "User does not have the required roles"

    async def has_permission(self, source: t.Any, info: Info, **kwargs) -> bool:
        user: BaseUser = info.context["user"]
        keys = build_role_payload(user, info.path, info.selected_fields)
        return user.is_authenticated
