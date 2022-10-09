import sys, asyncio

import pytest

from main import load_models
from db import create_engine, get_session_factory, BaseModel


@pytest.fixture(scope="session")
def event_loop():
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


DEFAULT_TEST_DB_DSN = "sqlite+aiosqlite:///:memory:"

DEFAULT_TEST_DB_SESSION_OPTIONS = {
    "autocommit": False,
    "expire_on_commit": False,
    "autoflush": False,
}

DEFAULT_TEST_DB_ECHO = False


@pytest.fixture(scope="session")
async def db_engine():
    load_models()
    _engine = await create_engine(DEFAULT_TEST_DB_DSN, {}, echo=DEFAULT_TEST_DB_ECHO)

    async with _engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    async with _engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        yield conn
        await conn.rollback()

    _engine.sync_engine.dispose()


@pytest.fixture(scope="session")
async def db_session(db_engine):
    session_factory = await get_session_factory(db_engine)
    async with session_factory() as _session:
        yield _session
        await _session.rollback()
