# ReservationRepository객체
#     def create(예약_항목_생성에_필요한_데이터):
#         새_예약_항목 = 영속_데이터_생성(예약_항목_생성에_필요한_데이터) 영속_데이터_저장(새_예약_항목)
#         새_예약_항목.id = 고유한_일련번호_값
#     return 새_예약_항목
#
#     def findall():
#         return list(저장된_영속 데이터들)


items = []


class ReservationRepository:
    _items: list

    def __init__(self):
        self._items = items

    def create(self, payload):
        obj = payload
        obj.id = len(self._items) + 1
        self._items.append(obj)
        return obj

    def findall(self):
        return self._items
