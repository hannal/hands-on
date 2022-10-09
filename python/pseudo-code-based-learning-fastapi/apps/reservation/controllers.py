from fastapi import APIRouter

from . import services
from .repositories import ReservationRepository, Reservation


router = APIRouter()


@router.get("/reservation/reservations", response_model=list[Reservation])
def reservations():
    repository = ReservationRepository()
    return services.reservations(None, repository)
