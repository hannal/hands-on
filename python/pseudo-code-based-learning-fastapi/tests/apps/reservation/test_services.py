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
    items = [
        repository.create(ReservationCreatePayload()),
        repository.create(ReservationCreatePayload()),
    ]

    # - 수행 (When)
    #   - 예약 가능한 세션 목록을 가져오기
    result = reservations(user, repository)

    # - 기대하는 결과 (Then)
    #   - 예약 항목 2개를 목록으로 반환
    result_set = frozenset(result)
    expected_set = frozenset(items)
    assert result_set & expected_set == expected_set