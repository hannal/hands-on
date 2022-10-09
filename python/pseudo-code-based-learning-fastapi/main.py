from fastapi import FastAPI

from apps.reservation.controllers import router as reservation_router
from libs.fastapi.error_handlers import setup_error_handlers
from db import create_engine, dispose_engines, create_all_models, DB_DSN

app = FastAPI()

app.include_router(reservation_router)
# app.include_router(reservation_router, prefix="/reservation")

setup_error_handlers(app)


@app.on_event("startup")
async def startup_event():
    load_models()

    await create_engine(DB_DSN, echo=False)
    await create_all_models(DB_DSN)


def load_models():
    from apps.reservation import models  # noqa


@app.on_event("shutdown")
async def shutdown_event():
    await dispose_engines()
