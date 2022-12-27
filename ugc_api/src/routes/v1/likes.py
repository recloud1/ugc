from uuid import UUID

import fastapi
from dependencies.auth import UserAuthorized
from fastapi import Depends, Path
from internal.likes import movie_like_crud
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.auth import UserInfo
from schemas.base import StatusResponse
from schemas.likes import MovieLikeCount, MovieLikeCreate
from utils.db_session import get_mongo_session

likes = fastapi.APIRouter()


@likes.get(
    "/{movie_id}/count",
    response_model=MovieLikeCount,
    summary="Получение количества лайков фильма",
    description="",
)
async def get_film_like_count(
    movie_id: str = Path(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> MovieLikeCount:
    """
    Получение количества лайков и дизлайков определенного фильма
    """

    movie_likes, movie_dislikes = await movie_like_crud.count(session, movie_id)

    return MovieLikeCount(movie_id=movie_id, likes=movie_likes, dislikes=movie_dislikes)


@likes.post("{movie_id}/add", response_model=StatusResponse)
async def create_film_like(
    movie_id: UUID = Path(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> StatusResponse:
    """
    Добавление лайка к фильму
    """
    await movie_like_crud.create(
        session, MovieLikeCreate(movie_id=movie_id, user_id=author.id)
    )

    return StatusResponse()


@likes.post("{movie_id}/remove", response_model=StatusResponse)
async def delete_film_like(
    movie_id: str = Path(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> StatusResponse:
    """
    Удаление лайка
    """
    movie_like = await movie_like_crud.find(session, str(author.id), movie_id)

    if not movie_like:
        return StatusResponse()

    await movie_like_crud.delete(session, movie_like["_id"])

    return StatusResponse()
