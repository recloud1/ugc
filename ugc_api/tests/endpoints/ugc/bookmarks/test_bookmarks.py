from http import HTTPStatus
from uuid import uuid4

from endpoints.conftest import USER_ID
from endpoints.ugc.bookmarks.requests import (
    create_bookmark,
    delete_bookmark,
    get_bookmarks,
)


async def test_create_bookmark(app_fixture):
    movie_id = str(uuid4())
    response, data = await create_bookmark(app_fixture, movie_id=movie_id)

    assert response.status_code == HTTPStatus.CREATED, data
    assert data["movieId"] == movie_id, data


async def test_get_bookmarks(app_fixture):
    _, bookmark = await create_bookmark(app_fixture)

    response, data = await get_bookmarks(app_fixture)

    assert response.status_code == HTTPStatus.OK, data
    assert len(data["data"]) > 0, data


async def test_remove_bookmark(app_fixture):
    movie_id = str(uuid4())
    _, bookmark = await create_bookmark(app_fixture, movie_id=movie_id)

    response, data = await delete_bookmark(app_fixture, movie_id)

    _, user_data = await get_bookmarks(app_fixture, user_id=USER_ID)
    assert response.status_code == HTTPStatus.OK, data
    assert len(user_data["data"]) == 0, user_data
