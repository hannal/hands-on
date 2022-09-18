import datetime

import strawberry
from strawberry.types import Info

from fastapi_authz import db
from . import models
from . import permissions


async def get_user_roles(root: "User", info: Info) -> list["UserRole"]:
    db_session = info.context["db_session"]
    # print("1" * 80)
    # print(info.path)
    # print(info.selected_fields)

    stmt = (
        db.select(models.User)
        .where(models.User.id == root.id)
        .options(db.selectinload(models.User.roles))
    )
    result = await db_session.execute(stmt)

    return [UserRole(id=_o.id, name=_o.name) for _o in result.scalar_one().roles]


async def get_users(info: Info) -> list["User"]:
    db_session = info.context["db_session"]
    # print("2" * 80)
    # print(info.path)
    # print(info.selected_fields)

    stmt = db.select(models.User).options(db.selectinload(models.User.roles))
    result = await db_session.execute(stmt)

    return [
        User(
            id=_o.id,
            username=_o.username,
            created_at=_o.created_at,
            updated_at=_o.updated_at,
        )
        for _o in result.scalars()
    ]


async def get_user(user_id: int, info: Info) -> "User":
    db_session = info.context["db_session"]

    stmt = (
        db.select(models.User)
        .where(models.User.id == user_id)
        .options(db.selectinload(models.User.roles))
    )
    result = await db_session.execute(stmt)
    _o = await result.scalars.one()

    return User(
        id=_o.id,
        username=_o.username,
        created_at=_o.created_at,
        updated_at=_o.updated_at,
    )


@strawberry.type
class UserRole:
    id: int
    name: str


@strawberry.federation.type(keys=["id"])
class User:
    id: int
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    roles: list[UserRole] = strawberry.field(
        resolver=get_user_roles,
        permission_classes=[permissions.IsAuthenticated, permissions.HasRoles],
    )


@strawberry.type
class Query:
    users: list[User] = strawberry.field(
        resolver=get_users,
        permission_classes=[permissions.IsAuthenticated, permissions.HasRoles],
    )
    get_user: User = strawberry.field(
        resolver=get_user,
        permission_classes=[permissions.IsAuthenticated, permissions.HasRoles],
    )


@strawberry.type
class Mutation:
    add_users: list[User] = strawberry.field(resolver=lambda: [User("2")])


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        User,
        UserRole,
    ],
)
