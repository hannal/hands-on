from apps.reservation.controllers import 예약가능한세션목록가져오기


def test_예약가능한세션목록가져오기():
    # - 주어진 조건 (Given)
    #   - 로그인 한 고객
    #   - 예약 항목 2개
    user = "로그인 한 고객"
    items = ["예약 항목 1", "예약 항목 2"]

    # - 수행 (When)
    #   - 예약 가능한 세션 목록을 가져오기
    result = 예약가능한세션목록가져오기(user)

    # - 기대하는 결과 (Then)
    #   - 예약 항목 2개를 목록으로 반환
    assert items == result
