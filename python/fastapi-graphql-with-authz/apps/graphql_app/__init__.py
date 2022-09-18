from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.exc import SQLAlchemyError

from fastapi_authz.settings import use_settings
from fastapi_authz.db import use_db_session, op, selectinload, AsyncSession
from fastapi_authz.auth import oauth2_bearer_scheme, User, AnonymousUser

from . import models  # noqa
from .schemas import schema


async def get_user(token: str, db_session: AsyncSession):
    if not token:
        return AnonymousUser()

    stmt = (
        op.select(models.User)
        .where(models.User.token == token)
        .options(selectinload(models.User.roles))
    )
    result = await db_session.execute(stmt)
    try:
        obj = result.scalar_one()
    except SQLAlchemyError:
        return AnonymousUser()

    return build_auth_user(obj)


async def get_router_context(
    db_session=Depends(use_db_session),
    app_settings=Depends(use_settings),
):
    return {
        "db_session": db_session,
        "app_settings": app_settings,
    }


router = GraphQLRouter(schema=schema, context_getter=get_router_context)


def build_auth_user(obj: models.User):
    return User(
        username=obj.username,
        roles=frozenset([_o.name for _o in obj.roles]),
        created_at=obj.created_at,
        updated_at=obj.updated_at,
    )
