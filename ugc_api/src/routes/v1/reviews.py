import fastapi
from dependencies.auth import UserAuthorized
from fastapi import Depends, Query
from internal.reviews import review_service
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.auth import UserInfo
from schemas.base import StatusResponse
from schemas.reviews import ReviewBare, ReviewList, ReviewUpdate
from utils.db_session import get_mongo_session

reviews = fastapi.APIRouter()


@reviews.get(
    "/",
    response_model=StatusResponse,
    summary="Получение рецензии",
    description="Производиться получение рецензии для фильма автора запроса",
)
async def get_reviews(
    movie_id: str | None = Query(None),
    user_id: str | None = Query(None),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
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
    response_model=StatusResponse,
    summary="Добавление рецензии для фильма",
    description="Производиться добавление рецензии для фильма автора запроса",
)
async def create_movie_review(
    data: ReviewUpdate,
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> ReviewBare:
    """
    Создание рецензии для фильма
    """
    review: dict = await review_service.create(
        session,
        data,
        user_id=author.id,
    )

    result = ReviewBare(
        id=review["_id"], user_id=review["user_id"], movie_id=review["movie_id"]
    )

    return result


@reviews.put(
    "/{movie_id}",
    response_model=StatusResponse,
    summary="Обновление рецензии для фильма",
    description="Производиться обновление рецензии для фильма автора запроса",
)
async def update_movie_review(
    data: ReviewUpdate,
    movie_id: int = Query(..., ge=1),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> ReviewBare:
    """
    Создание рецензии для фильма
    """
    review = await review_service.find(session, movie_id=movie_id, user_id=author.id)
    review = await review_service.update(session, review, data)

    result = ReviewBare(
        id=review["_id"], user_id=review["user_id"], movie_id=review["movie_id"]
    )

    return result


@reviews.delete(
    "/{movie_id}",
    response_model=StatusResponse,
    summary="Обновление рецензии для фильма",
    description="Производиться обновление рецензии для фильма автора запроса",
)
async def delete_movie_review(
    review_id: str = Query(..., ge=1),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> StatusResponse:
    """
    Удаление рецензии для фильма
    """
    await review_service.delete(session, review_id)

    return StatusResponse()
