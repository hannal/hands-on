import typing as t
from asyncio import current_task

from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship  # noqa
from sqlalchemy.sql.schema import *  # noqa
from sqlalchemy.sql.sqltypes import *  # noqa

from fastapi_authz.settings import Settings, use_settings

BaseModel = declarative_base()  # noqa

_factories: dict[str, async_scoped_session] = {}

_engines: dict[str, AsyncEngine] = {}

op = type(
    "op",
    (object,),
    {"insert": insert, "select": select, "update": update, "delete": delete},
)


async def create_engine(dsn: str, options: t.Optional[dict] = None, *, echo=False):
    _engine = _engines.get(dsn)
    if not _engine:
        _engine = create_async_engine(dsn, encoding="utf8", echo=echo, future=True)
        if options:
            _engine.execution_options(**options)
        _engines[dsn] = _engine
    return _engine


async def get_session_factory(dsn: str, options: t.Optional[dict] = None):
    _engine = _engines.get(dsn)
    if not _engine:
        return

    if dsn not in _factories:
        factory = async_scoped_session(
            sessionmaker(
                class_=AsyncSession,
                bind=_engine,
                **(options or {}),
            ),
            scopefunc=current_task,
        )

        _factories[dsn] = factory

    return _factories[dsn]


async def dispose_engines():
    for _engine in _engines.values():
        await _engine.dispose()


async def create_all_models(dsn: str):
    _engine = _engines.get(dsn)
    if not _engine:
        return

    async with _engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


async def use_db_session(settings: Settings = Depends(use_settings)):
    session_factory = await get_session_factory(
        settings.dsn, settings.db_session_options
    )
    async with session_factory() as _session:
        yield _session
