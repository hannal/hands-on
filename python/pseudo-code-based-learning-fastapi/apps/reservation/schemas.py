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
