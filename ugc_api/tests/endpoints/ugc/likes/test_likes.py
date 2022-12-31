from http import HTTPStatus
from uuid import uuid4

from endpoints.ugc.likes.requests import create_like, delete_like, get_like_count


async def test_create_like(app_fixture):
    response, data = await create_like(app_fixture, movie_id=str(uuid4()))

    assert response.status_code == HTTPStatus.CREATED, data


async def test_get_like_count(app_fixture):
    movie_id = str(uuid4())
    _, like_data = await create_like(app_fixture, movie_id=movie_id)

    response, data = await get_like_count(app_fixture, movie_id=movie_id)

    assert response.status_code == HTTPStatus.OK, data
    assert data["likes"] > 0, data


async def test_delete_like(app_fixture):
    movie_id = str(uuid4())
    _, like_data = await create_like(app_fixture, movie_id=movie_id)

    response, data = await delete_like(app_fixture, movie_id=movie_id)

    _, likes = await get_like_count(app_fixture, movie_id=movie_id)
    assert response.status_code == HTTPStatus.OK, data
    assert likes["likes"] == 0, likes
