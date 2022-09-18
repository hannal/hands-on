from apps.graphql_app import router as graphql_app_router

from . import app
from . import db
from .settings import load_settings

__all__ = ["app"]

app.include_router(graphql_app_router, prefix="/graphql-app")


@app.on_event("startup")
async def startup_event():
    settings = load_settings()

    await db.create_engine(
        settings.dsn,
        (settings.db_engine_options or {}),
        echo=settings.db_echo,
    )

    await db.create_all_models(settings.dsn)


@app.on_event("shutdown")
async def shutdown_event():
    await db.dispose_engines()
