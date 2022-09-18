import enum

import uvicorn
import typer
from alembic.config import main as alembic_main

cli = typer.Typer()


@enum.unique
class MigrateDirection(enum.Enum):
    UP = "upgrade"
    DOWN = "downgrade"


@cli.command(help="automatically generate a migration script")
def migrations(message: str = typer.Option(..., "-m", help="Migration message")):
    alembic_main(prog="alembic", argv=["revision", "--autogenerate", "-m", message])


@cli.command(help="run migrations")
def migrate(
    direction: MigrateDirection = typer.Argument(...),
    revision: str = typer.Option("head", "-r", help="Revision to migrate to"),
):
    alembic_main(prog="alembic", argv=[direction.value, revision])


@cli.command(help="run the application")
def localserver(host: str = "0.0.0.0", port: int = 8822, reload: bool = True):
    uvicorn.run("fastapi_authz.boot:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    cli()
