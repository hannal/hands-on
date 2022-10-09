import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.reservation.controllers import router


@pytest.fixture
def fastapi_app():
    app = FastAPI()
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
