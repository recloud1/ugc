from http import HTTPStatus
from uuid import uuid4

from endpoints.ugc.reviews.requests import (
    create_review,
    delete_review,
    get_reviews,
    update_review,
)


async def test_create_review(app_fixture):
    movie_id = str(uuid4())
    value = "some review value"

    response, data = await create_review(app_fixture, movie_id=movie_id, value=value)

    assert response.status_code == HTTPStatus.CREATED, data


async def test_get_reviews(app_fixture):
    movie_id = str(uuid4())
    value = "some review value"
    _, review_data = await create_review(app_fixture, movie_id=movie_id, value=value)

    response, data = await get_reviews(app_fixture, movie_id=movie_id)

    assert response.status_code == HTTPStatus.OK, data
    assert len(data["data"]) > 0, data


async def test_update_review(app_fixture):
    movie_id = str(uuid4())
    _, review_data = await create_review(
        app_fixture, movie_id=movie_id, value="some_value"
    )
    updated_value = "updated value"

    response, data = await update_review(
        app_fixture, movie_id=movie_id, value=updated_value
    )

    assert response.status_code == HTTPStatus.OK, data
    assert data["value"] == updated_value, data


async def test_delete_review(app_fixture):
    movie_id = str(uuid4())
    _, review_data = await create_review(
        app_fixture, movie_id=movie_id, value="some_value"
    )

    response, data = await delete_review(app_fixture, review_data["id"])

    _, get_data = await get_reviews(app_fixture, movie_id=movie_id)
    assert response.status_code == HTTPStatus.OK, data
    assert len(get_data["data"]) == 0, get_data
