from http import HTTPStatus

import fastapi
from fastapi import Depends, Query
from motor.motor_asyncio import AsyncIOMotorClient

from dependencies.auth import user_authorized
from internal.reviews import review_service
from schemas.auth import UserInfo
from schemas.base import StatusResponse
from schemas.reviews import ReviewBare, ReviewCreate, ReviewList, ReviewUpdate
from utils.db_session import get_mongo_session

reviews = fastapi.APIRouter()


@reviews.get(
    "/",
    response_model=ReviewList,
    summary="Получение рецензии",
    description="Производиться получение рецензии для фильма автора запроса",
)
async def get_reviews(
    movie_id: str | None = Query(None),
    user_id: str | None = Query(None),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(user_authorized),
) -> ReviewList:
    """
    Получение всех рецензий
    """
    review: list[dict] = await review_service.get_multi(
        session, user_id=user_id, movie_id=movie_id
    )

    result = [
        ReviewBare(
            id=i["_id"], user_id=i["user_id"], movie_id=i["movie_id"], value=i["value"]
        )
        for i in review
    ]

    return ReviewList(data=result)


@reviews.post(
    "/",
    response_model=ReviewBare,
    summary="Добавление рецензии для фильма",
    description="Производиться добавление рецензии для фильма автора запроса",
    status_code=HTTPStatus.CREATED,
)
async def create_movie_review(
    data: ReviewCreate,
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(user_authorized),
) -> ReviewBare:
    """
    Создание рецензии для фильма
    """
    review: dict = await review_service.create(
        session,
        data,
        user_id=str(author.id),
    )

    result = ReviewBare(
        id=str(review["_id"]),
        user_id=review["user_id"],
        movie_id=review["movie_id"],
        value=review["value"],
    )

    return result


@reviews.put(
    "/",
    response_model=ReviewBare,
    summary="Обновление рецензии для фильма",
    description="Производиться обновление рецензии для фильма автора запроса",
)
async def update_movie_review(
    data: ReviewUpdate,
    movie_id: str = Query(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(user_authorized),
) -> ReviewBare:
    """
    Обновление рецензии для фильма
    """
    review = await review_service.find(
        session, movie_id=movie_id, user_id=str(author.id)
    )
    review = await review_service.update(session, review["_id"], data)

    result = ReviewBare(
        id=str(review["_id"]),
        user_id=review["user_id"],
        movie_id=review["movie_id"],
        value=review["value"],
    )

    return result


@reviews.delete(
    "/",
    response_model=StatusResponse,
    summary="Удаление рецензии для фильма",
    description="Производиться удаление рецензии для фильма автора запроса",
)
async def delete_movie_review(
    review_id: str = Query(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(user_authorized),
) -> StatusResponse:
    """
    Удаление рецензии для фильма
    """
    await review_service.delete(session, review_id)

    return StatusResponse()
