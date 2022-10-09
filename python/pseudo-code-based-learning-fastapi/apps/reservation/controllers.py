from fastapi import APIRouter

from . import services
from .repositories import ReservationRepository, Reservation


router = APIRouter(prefix="/reservation")


@router.get("/reservations", response_model=list[Reservation])
def reservations():
    repository = ReservationRepository()
    return services.reservations(None, repository)
