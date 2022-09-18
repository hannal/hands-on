import typing as t
import abc
import datetime

import pydantic as pd
from fastapi.security import OAuth2PasswordBearer

oauth2_bearer_scheme = OAuth2PasswordBearer(tokenUrl="bearer")


class BaseUser(metaclass=abc.ABCMeta):
    username: str | None
    roles: frozenset[str]
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None

    @property
    def is_authenticated(self) -> bool:
        raise NotImplementedError


class User(BaseUser, pd.BaseModel):
    username: str
    roles: t.Optional[frozenset[str]] = pd.Field(default_factory=frozenset)
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @property
    def is_authenticated(self) -> bool:
        return True


class AnonymousUser(BaseUser):
    @property
    def username(self):
        return None

    @property
    def created_at(self):
        return None

    @property
    def updated_at(self):
        return None

    @property
    def roles(self) -> frozenset[str]:
        return frozenset()

    @property
    def is_authenticated(self) -> bool:
        return False
