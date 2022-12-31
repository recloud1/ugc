from http import HTTPStatus

import fastapi
from fastapi import Depends, Query
from motor.motor_asyncio import AsyncIOMotorClient

from dependencies.auth import user_authorized
from internal.likes import movie_like_crud
from schemas.auth import UserInfo
from schemas.base import StatusResponse
from schemas.likes import MovieLikeCount, MovieLikeCreate
from utils.db_session import get_mongo_session

likes = fastapi.APIRouter()


@likes.get(
    "/",
    response_model=MovieLikeCount,
    summary="Получение количества лайков фильма",
    description="",
)
async def get_film_like_count(
    movie_id: str = Query(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(user_authorized),
) -> MovieLikeCount:
    """
    Получение количества лайков и дизлайков определенного фильма
    """

    movie_likes, movie_dislikes = await movie_like_crud.count(session, movie_id)

    return MovieLikeCount(movie_id=movie_id, likes=movie_likes, dislikes=movie_dislikes)


@likes.post("/", response_model=StatusResponse, status_code=HTTPStatus.CREATED)
async def create_film_like(
    data: MovieLikeCreate,
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(user_authorized),
) -> StatusResponse:
    """
    Добавление лайка к фильму
    """
    await movie_like_crud.create(session, data, user_id=str(author.id))

    return StatusResponse()


@likes.delete("/", response_model=StatusResponse)
async def delete_film_like(
    movie_id: str = Query(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(user_authorized),
) -> StatusResponse:
    """
    Удаление лайка
    """
    movie_like = await movie_like_crud.find(
        session, user_id=str(author.id), movie_id=movie_id
    )

    if not movie_like:
        return StatusResponse()

    await movie_like_crud.delete(session, movie_like["_id"])

    return StatusResponse()
