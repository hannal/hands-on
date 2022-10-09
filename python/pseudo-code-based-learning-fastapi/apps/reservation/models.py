from db import BaseModel, Column, BigInteger, Integer, DateTime, Boolean, Identity


class Reservation(BaseModel):
    __tablename__ = "reservations"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    scheduled_date = Column(DateTime, nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)

    def __hash__(self):
        return hash(id)

    def __repr__(self):
        return f"Reservation(id={self.id}, scheduled_date={self.scheduled_date}, is_available={self.is_available})"

    def __str__(self):
        return self.__repr__()
