import datetime

import pytest
from fastapi import status

from apps.reservation.repositories import (
    ReservationRepository,
    ReservationCreatePayload,
)


@pytest.mark.asyncio
@pytest.fixture(scope="session")
async def reservations_fixture():
    repository = ReservationRepository()
    payloads = [
        ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow()),
        ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow()),
    ]
    yield [await repository.create(_payload) for _payload in payloads]


def test_get_reservation_list(client, reservations_fixture):
    res = client.get(
        "/reservation/reservations",
        params={"scheduled_date": datetime.date.today()},
    )

    assert res.status_code == status.HTTP_200_OK
    data = res.json()

    result = frozenset([_o["id"] for _o in data])
    expected = frozenset([_o.id for _o in reservations_fixture])
    assert result & expected == expected


def test_cannot_get_reservation_list_with_invalid_scheduled_date(
    client, reservations_fixture
):
    res = client.get(
        "/reservation/reservations",
        params={"scheduled_date": datetime.date(2020, 1, 1)},
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "headers, expected_status_code",
    [
        [None, status.HTTP_401_UNAUTHORIZED],
        [{"Authorization": "Bearer hannal"}, status.HTTP_200_OK],
    ],
)
def test_get_reservation_list_without_auth(
    anonymous_client, headers, expected_status_code
):
    res = anonymous_client.get(
        "/reservation/reservations",
        params={"scheduled_date": datetime.date.today()},
        headers=headers,
    )
    assert res.status_code == expected_status_code
