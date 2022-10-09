import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from apps.reservation.repositories import (
    ReservationRepository,
    ReservationCreatePayload,
)


@pytest.fixture(scope="session")
def reservations_fixture():
    repository = ReservationRepository()
    payloads = [
        ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow()),
        ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow()),
    ]
    return [repository.create(_payload) for _payload in payloads]


def test_get_reservation_list(reservations_fixture):
    client = TestClient(app)
    res = client.get("/reservation/reservations")
    assert res.status_code == status.HTTP_200_OK
    data = res.json()

    result = frozenset([_o["id"] for _o in data])
    expected = frozenset([_o.id for _o in reservations_fixture])
    assert result & expected == expected
