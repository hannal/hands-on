import datetime
from unittest.mock import MagicMock

import pytest

from apps.reservation.repositories import (
    ReservationRepository,
    ReservationCreatePayload,
)


@pytest.mark.asyncio
async def test_repository_can_create_reservation_with_valid_payload():
    # 주어진 조건
    #   - 유효한 예약 항목 생성 데이터
    payload = ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow())

    # 수행
    #   - 예약 항목 생성
    repository = ReservationRepository()
    result = await repository.create(payload)

    # 기대하는 결과
    #   - 고유한 일련번호 값이 `id` 속성으로 부여된 새로운 객체 반환
    assert hasattr(result, "id")
    assert isinstance(result.id, int)


@pytest.mark.asyncio
async def test_repository_find_all_items_without_params():
    # 주어진 조건
    #   - 예약 항목 2개
    repository = ReservationRepository()
    payload = ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow())
    item = await repository.create(payload)

    # 수행
    #   - 예약 항목 목록을 가져오기
    result = await repository.findall()

    # 기대하는 결과
    #   - 저장된 예약 항목 전체를 목록으로 반환
    assert isinstance(item.id, int)
    assert len(result) > 0
    assert any([_o.id == item.id for _o in result])


@pytest.mark.asyncio
async def test_repository_find_all_available_items():
    repository = ReservationRepository()

    # 주어진 조건
    #   - 예약된 항목 1개
    #   - 예약 가능한 항목 1개
    for _is_available in [True, False]:
        _o = await repository.create(
            ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow())
        )
        _o.is_available = _is_available

    # 수행
    #   - 예약 항목 목록을 가져오기
    result = await repository.findall()

    # 기대하는 결과
    #   - 저장된 예약 가능 항목을 목록으로 반환
    assert any([not _o.is_available for _o in result]) is False
    assert all([_o.is_available for _o in result]) is True


@pytest.mark.asyncio
async def test_repository_find_all_items_by_scheduled_date(monkeypatch):
    repository = ReservationRepository()

    # 주어진 조건
    #   - 예약 항목 6개
    target_date = datetime.datetime.utcnow().replace(day=15) + datetime.timedelta(
        days=31
    )
    payloads = [
        ReservationCreatePayload(scheduled_date=target_date),
        ReservationCreatePayload(
            scheduled_date=target_date - datetime.timedelta(days=1)
        ),
        ReservationCreatePayload(scheduled_date=target_date),
        ReservationCreatePayload(
            scheduled_date=target_date + datetime.timedelta(days=1)
        ),
        # 기준 달 이후
        ReservationCreatePayload(
            scheduled_date=target_date + datetime.timedelta(days=31)
        ),
        # 기준 달 이전
        ReservationCreatePayload(
            scheduled_date=target_date - datetime.timedelta(days=31)
        ),
    ]
    unavailable_item, yesterday_item, *items = [
        await repository.create(_o) for _o in payloads
    ]
    unavailable_item.is_available = False

    # 수행
    #   - 지정한 달의 예약 항목 목록을 가져오기
    with monkeypatch.context() as _m:
        _mock_datetime = MagicMock(spec=datetime.datetime)
        _mock_datetime.utcnow.return_value = target_date
        _m.setattr(datetime, "datetime", _mock_datetime)

        result = frozenset(await repository.findall(scheduled_date=target_date.date()))

    # 기대하는 결과
    #   - 지정한 달의 예약 가능 항목만 목록으로 반환
    assert all(
        [
            _o.is_available
            and _o.scheduled_date.year == target_date.year
            and _o.scheduled_date.month == target_date.month
            for _o in result
        ]
    )
    #   - 지정한 달이 이번 달인 경우 오늘부터 말일까지 반환
    assert yesterday_item not in result
