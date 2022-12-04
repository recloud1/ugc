import requests
from fastapi import security, Depends

from core.config import envs
from schemas.auth import UserInfo


def jwt_token_dep(
        token: security.HTTPAuthorizationCredentials = Depends(security.HTTPBearer(bearerFormat='Bearer'))
) -> str:
    return token.credentials


class UserAuthorized:
    def __init__(self):
        """
        Зависимость для работы с разрешениями для http endpoint'ов.
        """
    def __call__(self, token: str = Depends(jwt_token_dep)) -> UserInfo:
        url = envs.external.auth
        data = {'token': token}
        data = requests.post(url=url, json=data).json()
        result = UserInfo(**data)

        return result
