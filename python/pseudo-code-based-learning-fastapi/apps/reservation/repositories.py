import datetime

import pydantic

# ReservationRepository객체
#     def create(예약_항목_생성에_필요한_데이터):
#         새_예약_항목 = 영속_데이터_생성(예약_항목_생성에_필요한_데이터) 영속_데이터_저장(새_예약_항목)
#         새_예약_항목.id = 고유한_일련번호_값
#     return 새_예약_항목
#
#     def findall():
#         return list(저장된_영속 데이터들)


items = []


class ReservationCreatePayload(pydantic.BaseModel):
    scheduled_date: datetime.datetime


class Reservation(pydantic.BaseModel):
    id: int
    scheduled_date: datetime.datetime
    is_available: bool

    def __hash__(self):
        return hash(id)


class ReservationRepository:
    _items: list[Reservation]

    def __init__(self):
        self._items = items

    def create(self, payload: ReservationCreatePayload) -> Reservation:
        obj = Reservation(
            id=len(self._items) + 1,
            is_available=True,
            **payload.dict(),
        )
        self._items.append(obj)
        return obj

    def findall(self):
        return [_o for _o in self._items if _o.is_available]
