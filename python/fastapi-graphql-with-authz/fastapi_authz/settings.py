import typing as t
import dataclasses

from dotenv import load_dotenv, dotenv_values

__all__ = [
    "use_settings",
    "load_settings",
    "Settings",
]

load_dotenv()

_ENVS = dotenv_values()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Settings:
    debug: bool
    dsn: str
    db_echo: bool = True
    db_engine_options: t.Optional[dict] = None
    db_session_options: t.Optional[dict] = None


_local_settings = Settings(
    debug=True,
    dsn="sqlite+aiosqlite:///./local.db",
    db_session_options={
        "autocommit": False,
        "expire_on_commit": False,
        "autoflush": False,
    },
)


_test_settings = Settings(
    debug=True,
    dsn="sqlite+aiosqlite:///:memory:",
    db_session_options={
        "autocommit": False,
        "expire_on_commit": False,
        "autoflush": False,
    },
)


async def use_settings():
    yield load_settings()


def load_settings(
    env_name: t.Optional[str] = _ENVS.get("ENV_NAME", "local")
) -> Settings:
    for _k, _v in globals().items():
        if _k == f"_{env_name}_settings" and isinstance(_v, Settings):
            return _v

    raise ImportError(f"settings for {env_name} not found")
