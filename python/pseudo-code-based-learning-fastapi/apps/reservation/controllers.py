import datetime

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from . import services
from .repositories import ReservationRepository, Reservation


router = APIRouter(prefix="/reservation")


@router.get("/reservations", response_model=list[Reservation])
def reservations(scheduled_date: datetime.date):
    repository = ReservationRepository()
    try:
        return services.reservations(None, repository, scheduled_date)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
