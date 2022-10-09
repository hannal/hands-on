import datetime

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException

from db import use_db_session
from libs.fastapi import dependencies
from .repositories import BaseReservationRepository, ReservationDbRepository
from .schemas import Reservation
from . import services

router = APIRouter(prefix="/reservation")


async def use_reservation_repository(db_session=Depends(use_db_session)):
    yield ReservationDbRepository(db_session=db_session)


@router.get(
    "/reservations",
    response_model=list[Reservation],
    dependencies=[Depends(dependencies.use_user)],
)
async def reservations(
    scheduled_date: datetime.date,
    repository: BaseReservationRepository = Depends(use_reservation_repository),
):
    try:
        return await services.reservations(None, repository, scheduled_date)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
