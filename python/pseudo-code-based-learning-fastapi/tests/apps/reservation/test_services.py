import datetime

import pytest

from apps.reservation.services import reservations
from apps.reservation.repositories import (
    ReservationRepository,
    ReservationCreatePayload,
)


def test_reservations():
    # - 주어진 조건 (Given)
    #   - 로그인 한 고객
    #   - 예약 항목 2개
    user = "로그인 한 고객"
    repository = ReservationRepository()
    payloads = [
        ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow()),
        ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow()),
    ]
    items = [repository.create(_payload) for _payload in payloads]

    # - 수행 (When)
    #   - 예약 가능한 세션 목록을 가져오기
    scheduled_date = datetime.date.today()
    result = reservations(user, repository, scheduled_date)

    # - 기대하는 결과 (Then)
    #   - 예약 항목 2개를 목록으로 반환
    result_set = frozenset(result)
    expected_set = frozenset(items)
    assert result_set & expected_set == expected_set


def test_reservations_cannot_get_list_with_invalid_scheduled_date():
    # - 주어진 조건 (Given)
    #   - 로그인 한 고객
    user = "로그인 한 고객"
    repository = ReservationRepository()
    scheduled_date = datetime.date(2020, 1, 1)

    # - 기대하는 결과 (Then)
    #   - 잘못된 요청하지 말라는 오류 응답
    with pytest.raises(ValueError):
        # - 수행 (When)
        #   - 지난 달을 지정하여 예약 가능한 세션 목록을 가져오기
        reservations(user, repository, scheduled_date)


def test_reservations_can_get_list_with_valid_scheduled_date():
    repository = ReservationRepository()

    # - 주어진 조건 (Given)
    #   - 로그인 한 고객
    #   - 예약 항목 3개
    user = "로그인 한 고객"
    target_date = datetime.datetime.utcnow() + datetime.timedelta(days=61)
    payloads = [
        ReservationCreatePayload(scheduled_date=target_date),
        ReservationCreatePayload(scheduled_date=target_date),
        # 기준 달 이후
        ReservationCreatePayload(
            scheduled_date=target_date + datetime.timedelta(days=31)
        ),
        # 기준 달 이전
        ReservationCreatePayload(
            scheduled_date=target_date - datetime.timedelta(days=31)
        ),
    ]
    items = [repository.create(_o) for _o in payloads]
    items[0].is_available = False

    # - 수행 (When)
    #   - 지난 달을 지정하여 예약 가능한 세션 목록을 가져오기
    result = reservations(user, repository, target_date)

    # - 기대하는 결과 (Then)
    #   - 지정한 달의 예약 가능 항목만 목록으로 반환
    expected = repository.findall(scheduled_date=target_date)
    assert frozenset(result) == frozenset(expected)
