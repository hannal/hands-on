import datetime

from apps.reservation.repositories import BaseReservationRepository


async def reservations(
    user, repository: BaseReservationRepository, scheduled_date: datetime.date
):
    scheduled_date = validate_scheduled_date(scheduled_date)
    return await repository.findall(scheduled_date=scheduled_date)


def validate_scheduled_date(v: datetime.date):
    today = datetime.date.today()
    if v.year < today.year or v.month < today.month:
        raise ValueError("오늘이거나 이후 일자여야 합니다.")
    if v.year == today.year and v.month == today.month:
        return today
    return v
