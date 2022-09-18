import sys
import asyncio

import pytest
from fastapi.testclient import TestClient

from fastapi_authz import app, boot  # noqa
from fastapi_authz.settings import load_settings, Settings
from fastapi_authz import db


@pytest.fixture(scope="session")
def event_loop():
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def http_client():
    yield TestClient(app)


@pytest.fixture(scope="session")
async def app_settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
async def db_engine(app_settings: Settings):
    _engine = await db.create_engine(
        app_settings.dsn,
        app_settings.db_engine_options or {},
        echo=app_settings.db_echo,
    )

    async with _engine.begin() as conn:
        await conn.run_sync(db.BaseModel.metadata.drop_all)

    async with _engine.begin() as conn:
        await conn.run_sync(db.BaseModel.metadata.create_all)
        yield conn
        await conn.rollback()

    _engine.sync_engine.dispose()


@pytest.fixture
async def db_session(db_engine, app_settings: Settings):
    session_factory = await db.get_session_factory(
        app_settings.dsn, app_settings.db_session_options or {}
    )
    async with session_factory() as _session:
        yield _session
