import datetime

from apps.reservation.repositories import ReservationRepository


def reservations(
    user, repository: ReservationRepository, scheduled_date: datetime.date
):
    validate_scheduled_date(scheduled_date)
    return repository.findall()


def validate_scheduled_date(v: datetime.date):
    today = datetime.date.today()
    if v.year < today.year or v.month < today.month:
        raise ValueError("오늘이거나 이후 일자여야 합니다.")
    if v.year == today.year and v.month == today.month:
        return today
    return v
