import datetime

from apps.reservation.repositories import (
    ReservationRepository,
    ReservationCreatePayload,
)


def test_repository_can_create_reservation_with_valid_payload():
    # 주어진 조건
    #   - 유효한 예약 항목 생성 데이터
    payload = ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow())

    # 수행
    #   - 예약 항목 생성
    repository = ReservationRepository()
    result = repository.create(payload)

    # 기대하는 결과
    #   - 고유한 일련번호 값이 `id` 속성으로 부여된 새로운 객체 반환
    assert hasattr(result, "id")
    assert isinstance(result.id, int)


def test_repository_find_all_items_without_params():
    # 주어진 조건
    #   - 예약 항목 2개
    repository = ReservationRepository()
    payload = ReservationCreatePayload(scheduled_date=datetime.datetime.utcnow())
    item = repository.create(payload)

    # 수행
    #   - 예약 항목 목록을 가져오기
    result = repository.findall()

    # 기대하는 결과
    #   - 저장된 예약 항목 전체를 목록으로 반환
    assert isinstance(item.id, int)
    assert len(result) > 0
    assert any([_o.id == item.id for _o in result])
