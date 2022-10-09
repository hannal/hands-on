from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
import pydantic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(pydantic.BaseModel):
    username: str
    is_staff: bool


_mock_users_by_token = {
    "hannal": User(username="hannal", is_staff=False),
}


async def use_user(token: str = Depends(oauth2_scheme)) -> User:
    if _user := _mock_users_by_token.get(token):
        return _user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
