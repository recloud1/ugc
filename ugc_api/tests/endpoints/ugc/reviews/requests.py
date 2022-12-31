from typing import Tuple

from endpoints.core.constants import ApiRoutes, RequestMethods
from endpoints.utils.requests import api_request
from starlette.responses import Response
from starlette.testclient import TestClient


async def get_reviews(
    client: TestClient,
    user_id: str | None = None,
    movie_id: str | None = None,
    with_check: bool = False,
) -> Tuple[Response, dict]:
    params = {}
    if user_id:
        params["user_id"] = user_id
    if movie_id:
        params["movie_id"] = movie_id

    response, data = await api_request(
        client,
        RequestMethods.get,
        ApiRoutes.bookmarks,
        query_params=params,
        with_check=with_check,
    )

    return response, data


async def create_review(
    client: TestClient, movie_id: str, value: str, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.post,
        ApiRoutes.reviews,
        with_check=with_check,
        data={"movie_id": movie_id, "value": value},
    )

    return response, data


async def update_review(
    client: TestClient, movie_id: str, value: str, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.put,
        ApiRoutes.reviews,
        with_check=with_check,
        query_params={"movie_id": movie_id},
        data={"value": value},
    )

    return response, data


async def delete_review(
    client: TestClient, review_id: str, with_check: bool = False
) -> Tuple[Response, dict]:
    response, data = await api_request(
        client,
        RequestMethods.delete,
        ApiRoutes.reviews,
        query_params={"review_id": review_id},
        with_check=with_check,
    )

    return response, data
