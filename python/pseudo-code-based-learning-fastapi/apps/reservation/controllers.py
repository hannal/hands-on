import datetime

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException

from libs.fastapi import dependencies
from . import services
from .repositories import ReservationRepository, Reservation


router = APIRouter(prefix="/reservation")


@router.get(
    "/reservations",
    response_model=list[Reservation],
    dependencies=[Depends(dependencies.use_user)],
)
async def reservations(scheduled_date: datetime.date):
    repository = ReservationRepository()
    try:
        return await services.reservations(None, repository, scheduled_date)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
