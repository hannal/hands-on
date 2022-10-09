from fastapi import FastAPI

from apps.reservation.controllers import router as reservation_router

app = FastAPI()

app.include_router(reservation_router)
