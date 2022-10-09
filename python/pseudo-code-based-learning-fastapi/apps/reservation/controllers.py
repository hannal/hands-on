from fastapi import APIRouter, Depends

from db import use_db_session
from libs.fastapi import dependencies
from libs.fastapi.dependencies import User
from .repositories import BaseReservationRepository, ReservationDbRepository
from .schemas import Reservation, ReservationListParam
from . import services

router = APIRouter(prefix="/reservation")


async def use_reservation_repository(db_session=Depends(use_db_session)):
    yield ReservationDbRepository(db_session=db_session)


@router.get("/reservations", response_model=list[Reservation])
async def reservations(
    user: User = Depends(dependencies.use_user),
    params: ReservationListParam = Depends(),
    repository: BaseReservationRepository = Depends(use_reservation_repository),
):
    return await services.reservations(user, repository, params.scheduled_date)
