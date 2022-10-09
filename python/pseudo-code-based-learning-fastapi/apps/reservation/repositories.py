import typing as t
import abc
import datetime

from db import AsyncSession, select, Select, func, extract
from apps.reservation.schemas import ReservationCreatePayload, Reservation
from apps.reservation.models import Reservation as ReservationModel

# ReservationRepository객체
#     def create(예약_항목_생성에_필요한_데이터):
#         새_예약_항목 = 영속_데이터_생성(예약_항목_생성에_필요한_데이터) 영속_데이터_저장(새_예약_항목)
#         새_예약_항목.id = 고유한_일련번호_값
#     return 새_예약_항목
#
#     def findall(지정한_일자):
#         return list(저장된_영속 데이터들 중에서 지정한일자에 속한 달 또는 이번 달에서 오늘부터 말일까지)


items = []


class BaseReservationRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def create(self, payload: ReservationCreatePayload) -> Reservation:
        raise NotImplementedError

    @abc.abstractmethod
    async def findall(
        self, *, scheduled_date: t.Optional[datetime.date] = None
    ) -> list[Reservation]:
        raise NotImplementedError


class ReservationFakeRepository(BaseReservationRepository):
    _items: list[Reservation]

    def __init__(self):
        super().__init__()
        self._items = items

    async def create(self, payload: ReservationCreatePayload) -> Reservation:
        obj = Reservation(
            id=len(self._items) + 1,
            is_available=True,
            **payload.dict(),
        )
        self._items.append(obj)
        return obj

    async def findall(
        self, *, scheduled_date: t.Optional[datetime.date] = None
    ) -> list[Reservation]:
        filtered = filter(lambda _o: _o.is_available, self._items)

        if isinstance(scheduled_date, datetime.date):
            filtered = self._filter_by_scheduled_date(scheduled_date, filtered)
        return list(filtered)

    @staticmethod
    def _filter_by_scheduled_date(
        scheduled_date: datetime.date, objs: filter | list[Reservation]
    ) -> filter:
        filtered = filter(
            lambda _o: _o.scheduled_date.year == scheduled_date.year,
            objs,
        )
        filtered = filter(
            lambda _o: _o.scheduled_date.month == scheduled_date.month,
            filtered,
        )

        today = datetime.datetime.utcnow().date()
        if scheduled_date == today:
            return filter(
                lambda _o: _o.scheduled_date.date() >= today,
                filtered,
            )
        return filtered


class ReservationDbRepository(BaseReservationRepository):
    _db_session: AsyncSession

    def __init__(self, db_session: AsyncSession):
        super().__init__()
        self._db_session = db_session

    async def create(self, payload: ReservationCreatePayload) -> Reservation:
        obj = ReservationModel(
            is_available=True,
            **payload.dict(),
        )
        self._db_session.add(obj)
        await self._db_session.commit()
        return Reservation.from_orm(obj)

    async def findall(
        self, *, scheduled_date: t.Optional[datetime.date] = None
    ) -> list[Reservation]:
        stmt = select(ReservationModel)
        if isinstance(scheduled_date, datetime.date):
            stmt = self._filter_by_scheduled_date(scheduled_date, stmt)

        result = await self._db_session.execute(stmt)
        return [Reservation.from_orm(_o) for _o in result.scalars().all()]

    @staticmethod
    def _filter_by_scheduled_date(
        scheduled_date: datetime.date, stmt: Select
    ) -> filter:
        stmt = stmt.where(
            extract("year", ReservationModel.scheduled_date) == scheduled_date.year,
            extract("month", ReservationModel.scheduled_date) == scheduled_date.month,
        )

        today = datetime.datetime.utcnow().date()
        if scheduled_date == today:
            stmt = stmt.where(func.date(ReservationModel.scheduled_date) >= today)
        return stmt
