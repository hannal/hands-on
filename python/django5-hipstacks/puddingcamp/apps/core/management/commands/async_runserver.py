from django.core.management.commands.runserver import Command as BaseCommand
from uvicorn.main import run as uvicorn_run


class Command(BaseCommand):
    default_port = "8000"
  
    def run(self, **options):
        use_reloader = options["use_reloader"]
        uvicorn_run(
            "puddingcamp.asgi:application",
            host=self.addr,
            port=int(self.port),
            reload=use_reloader,
        )
