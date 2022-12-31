from typing import Tuple
from uuid import uuid4

from endpoints.core.constants import ApiRoutes, RequestMethods
from endpoints.utils.requests import api_request
from starlette.responses import Response
from starlette.testclient import TestClient


async def get_bookmarks(
    client: TestClient, user_id: str | None = None, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.get,
        ApiRoutes.bookmarks,
        query_params={"user_id": user_id} if user_id else None,
        with_check=with_check,
    )

    return response, data


async def create_bookmark(
    client: TestClient, movie_id: str | None = None, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.post,
        ApiRoutes.bookmarks,
        with_check=with_check,
        data={
            "movie_id": movie_id or uuid4().hex,
        },
    )

    return response, data


async def delete_bookmark(
    client: TestClient, movie_id: str, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.delete,
        ApiRoutes.bookmarks,
        query_params={"movie_id": movie_id},
        with_check=with_check,
    )

    return response, data
