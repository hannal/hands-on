import datetime

from libs.fastapi.dependencies import User
from apps.reservation.repositories import BaseReservationRepository
from apps.reservation.schemas import validate_scheduled_date


async def reservations(
    user: User, repository: BaseReservationRepository, scheduled_date: datetime.date
):
    scheduled_date = validate_scheduled_date(scheduled_date)
    return await repository.findall(scheduled_date=scheduled_date)
