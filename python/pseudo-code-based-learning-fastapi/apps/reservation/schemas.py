import datetime

import pydantic


class ReservationCreatePayload(pydantic.BaseModel):
    scheduled_date: datetime.datetime


class Reservation(pydantic.BaseModel):
    id: int
    scheduled_date: datetime.datetime
    is_available: bool

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(id)


class ReservationListParam(pydantic.BaseModel):
    scheduled_date: datetime.date

    @pydantic.validator("scheduled_date", pre=True, always=True)
    def validate_scheduled_date(cls, v: datetime.date):
        return validate_scheduled_date(v)


def validate_scheduled_date(v: datetime.date):
    today = datetime.date.today()
    if v.year < today.year or v.month < today.month:
        raise ValueError("오늘이거나 이후 일자여야 합니다.")
    if v.year == today.year and v.month == today.month:
        return today
    return v
