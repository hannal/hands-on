from pathlib import Path

import typing as t
from asyncio import current_task
from collections import namedtuple

from sqlalchemy import delete, insert, select, update, func, extract, Identity  # noqa
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,  # noqa
    selectinload,  # noqa
)
from sqlalchemy.sql.schema import *  # noqa
from sqlalchemy.sql.sqltypes import *  # noqa
from sqlalchemy.sql.selectable import Select  # noqa

BaseModel = declarative_base()  # noqa

BASE_DIR = Path(__file__).parent

DB_DSN = f"sqlite+aiosqlite://{(BASE_DIR / 'db.sqlite3').as_posix()}"

DB_SESSION_OPTIONS = {
    "autocommit": False,
    "expire_on_commit": False,
    "autoflush": False,
}

_factories: dict[str, async_scoped_session] = {}

_engines: dict[str, AsyncEngine] = {}

op = namedtuple("Op", "insert, select, update, delete")(insert, select, update, delete)


async def create_engine(dsn: str, options: t.Optional[dict] = None, *, echo=False):
    _engine = _engines.get(dsn)
    if not _engine:
        _engine = create_async_engine(dsn, encoding="utf8", echo=echo, future=True)
        if options:
            _engine.execution_options(**options)
        _engines[dsn] = _engine
    return _engine


async def get_session_factory(engine_or_dsn: t.Optional[AsyncEngine | str] = None):
    if not engine_or_dsn:
        _engine = await create_engine(DB_DSN)
    elif isinstance(engine_or_dsn, str):
        _engine = await create_engine(engine_or_dsn)
    else:
        _engine = engine_or_dsn

    return async_scoped_session(
        sessionmaker(
            class_=AsyncSession,
            bind=_engine,
            **DB_SESSION_OPTIONS,
        ),
        scopefunc=current_task,
    )


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


async def use_db_session():
    session_factory = await get_session_factory(DB_DSN)
    async with session_factory() as _session:
        yield _session
