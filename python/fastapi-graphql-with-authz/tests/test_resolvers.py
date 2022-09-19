from unittest.mock import MagicMock
from textwrap import dedent

import pytest
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_authz import db
from apps.graphql_app import models, build_auth_user
from apps.graphql_app.schemas import schema
from fastapi_authz import auth


@pytest.fixture
def graphql_info(app_settings, db_session):
    mock = MagicMock(spec=Info)
    mock.context = {
        "db_session": db_session,
        "app_settings": app_settings,
        "user": auth.AnonymousUser(),
    }
    yield mock


@pytest.fixture
@pytest.mark.asyncio
async def users(db_session: AsyncSession):
    objs = [
        models.User(username="user1"),
        models.User(username="user2"),
    ]
    db_session.add_all(objs)

    await db_session.commit()

    stmt = db.op.select(models.User).options(db.selectinload(models.User.roles))
    result = await db_session.execute(stmt)
    users = result.scalars().all()
    yield users

    for _o in users:
        await db_session.delete(_o)
    await db_session.commit()


@pytest.fixture
@pytest.mark.asyncio
async def user_roles(db_session, users):
    objs = [
        models.UserRole(name="role1"),
        models.UserRole(name="role2"),
        models.UserRole(name="role3"),
    ]
    db_session.add_all(objs)

    await db_session.commit()

    stmt = db.op.select(models.UserRole)
    result = await db_session.execute(stmt)
    roles = result.scalars().all()

    yield roles

    for _o in roles:
        await db_session.delete(_o)
    await db_session.commit()


@pytest.mark.asyncio
async def test_query_users(db_session, graphql_info, users, user_roles):
    user = users[0]
    user.roles.extend(user_roles)
    db_session.add(user)
    await db_session.commit()

    graphql_info.context["user"] = build_auth_user(user)

    expected_users = frozenset([_o.id for _o in users])
    expected_roles = frozenset([(_o.id, _o.name) for _o in user.roles])

    query = dedent(
        """
        query MyQuery {
            users {
                id
                roles {
                    id
                    name
                }
            }
        }
        """
    )
    result = await schema.execute(query, context_value=graphql_info.context)
    assert result.errors is None

    result_users = frozenset([_o["id"] for _o in result.data["users"]])
    result_user = [_o for _o in result.data["users"] if _o["id"] == user.id][0]
    result_roles = frozenset([(_o["id"], _o["name"]) for _o in result_user["roles"]])

    assert result_users == expected_users
    assert result_roles == expected_roles


@pytest.mark.parametrize(
    "role_indexes, expected_authz_errors",
    [
        [[], True],
        [[0], True],
        [[1], True],
        [[0, 1], False],
    ],
)
@pytest.mark.asyncio
async def test_authorization_by_role(
    db_session,
    graphql_info,
    users,
    user_roles,
    role_indexes: list[int],
    expected_authz_errors,
):
    user = users[0]
    for _index in role_indexes:
        user.roles.append(user_roles[_index])
    db_session.add(user)
    await db_session.commit()

    graphql_info.context["user"] = build_auth_user(user)

    query = dedent(
        """
        query MyQuery {
            users {
                id
                roles {
                    id
                    name
                }
            }
        }
        """
    )
    result = await schema.execute(query, context_value=graphql_info.context)
    assert (result.errors is not None) is expected_authz_errors
