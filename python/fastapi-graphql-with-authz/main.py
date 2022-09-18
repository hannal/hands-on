import uvicorn
import typer

cli = typer.Typer()


@cli.command()
def migrations():
    pass


@cli.command()
def localserver(host: str = "0.0.0.0", port: int = 8822, reload: bool = True):
    uvicorn.run("boot.app:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    cli()
