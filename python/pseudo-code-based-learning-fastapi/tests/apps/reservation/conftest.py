import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from db import use_db_session, get_session_factory
from apps.reservation.controllers import router


@pytest.fixture
def fastapi_app(db_engine):
    async def testing_use_db_session():
        session_factory = await get_session_factory(db_engine)
        async with session_factory() as _session:
            yield _session

    app = FastAPI()
    app.dependency_overrides[use_db_session] = testing_use_db_session
    app.include_router(router)
    yield app


@pytest.fixture
def client(fastapi_app):
    client = TestClient(fastapi_app)
    client.headers.update({"Authorization": "Bearer hannal"})
    yield client


@pytest.fixture
def anonymous_client(fastapi_app):
    yield TestClient(fastapi_app)
