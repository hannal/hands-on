import dataclasses

from apps.reservation.repositories import ReservationRepository


@dataclasses.dataclass
class ReservationPayload:
    id: int | None = dataclasses.field(default=None)


def test_repository_can_create_reservation_with_valid_payload():
    # 주어진 조건
    #   - 유효한 예약 항목 생성 데이터
    payload = ReservationPayload()

    # 수행
    #   - 예약 항목 생성
    repository = ReservationRepository()
    result = repository.create(payload)

    # 기대하는 결과
    #   - 고유한 일련번호 값이 `id` 속성으로 부여된 새로운 객체 반환
    assert hasattr(result, "id")
    assert isinstance(result.id, int)
