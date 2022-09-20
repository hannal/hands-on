import typing as t
import abc
import datetime

import pydantic as pd
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)

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


def get_authorization_scheme_param(authorization_header_value: str) -> tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


class TokenAuthenticationBackend(AuthenticationBackend):
    _default_message = "Invalid authentication token"
    _backend_server_error_message = "Backend server error"

    async def authenticate(self, request):
        auth: str = request.headers.get("Authorization")
        if not auth:
            return None, AnonymousUser()

        scheme, token = get_authorization_scheme_param(auth)
        if not auth or scheme.lower() != "bearer":
            return None, AnonymousUser()

        if token != "hannal":
            return None, AnonymousUser()

        return self.build_auth_data(token)

    @staticmethod
    def build_auth_data(token: str) -> tuple[AuthCredentials, User]:
        cred = AuthCredentials(["authenticated"])
        user = User(
            username=token,
            roles=frozenset(["role1", "role2"]),
            created_at=datetime.datetime(2021, 7, 20, 0, 0, 0),
            updated_at=datetime.datetime(2022, 9, 21, 19, 0, 0),
        )
        return cred, user
