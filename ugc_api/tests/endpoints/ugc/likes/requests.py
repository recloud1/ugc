from typing import Tuple

from endpoints.core.constants import ApiRoutes, RequestMethods
from endpoints.utils.requests import api_request
from starlette.responses import Response
from starlette.testclient import TestClient


async def get_like_count(
    client: TestClient, movie_id: str, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.get,
        ApiRoutes.likes,
        query_params={"movie_id": movie_id},
        with_check=with_check,
    )

    return response, data


async def create_like(
    client: TestClient,
    movie_id: str,
    value: int = 10,
    with_check: bool = False,
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.post,
        ApiRoutes.likes,
        data={"movie_id": movie_id, "value": value},
        with_check=with_check,
    )

    return response, data


async def delete_like(
    client: TestClient, movie_id: str, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.delete,
        ApiRoutes.likes,
        query_params={"movie_id": movie_id},
        with_check=with_check,
    )

    return response, data
