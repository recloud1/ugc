import fastapi
from bson import ObjectId
from core.crud.exceptions import ObjectNotExists
from dependencies.auth import UserAuthorized
from fastapi import Depends, Query
from internal.bookmarks import bookmark_service
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.auth import UserInfo
from schemas.base import StatusResponse
from schemas.bookmarks import BookmarkBare, BookmarkCreate, BookmarkList
from utils.db_session import get_mongo_session
from utils.utils import convert_uuid


bookmarks = fastapi.APIRouter()


@bookmarks.get(
    "/",
    response_model=BookmarkList,
    summary="Получение списка закладок",
    description="Производиться получение списка закладок автора запроса",
)
async def get_bookmarks(
    user_id: str | None = Query(None),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> BookmarkList:
    """
    Получение списка закладок пользователя
    """
    user_id = user_id or author.id

    bookmark: BookmarkList = await bookmark_service.get_multi(
        session, user_id=convert_uuid(user_id)
    )

    result = [
        BookmarkBare(id=str(i["_id"]), user_id=i["user_id"], movie_id=i["movie_id"])
        for i in bookmark
    ]

    return BookmarkList(data=result)


@bookmarks.post(
    "/",
    response_model=StatusResponse,
    summary="Добавление рецензии для фильма",
    description="Производиться добавление рецензии для фильма автора запроса",
)
async def create_bookmark(
    data: BookmarkCreate,
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> StatusResponse:
    """
    Создание закладки
    """
    await bookmark_service.create(
        session,
        data,
        user_id=convert_uuid(author.id),
    )

    return StatusResponse()


@bookmarks.delete(
    "/{movie_id}",
    response_model=StatusResponse,
    summary="Удаление фильма из закладок пользователя",
    description="Производиться удаление фильма из закладок пользователя",
)
async def delete_movie_review(
    movie_id: str = Query(...),
    session: AsyncIOMotorClient = Depends(get_mongo_session),
    author: UserInfo = Depends(UserAuthorized()),
) -> StatusResponse:
    """
    Удаление рецензии для фильма
    """
    bookmark = await bookmark_service.find(
        session, movie_id=movie_id, user_id=convert_uuid(author.id)
    )
    if not bookmark:
        raise ObjectNotExists("Закладка не найдена")

    bookmark: BookmarkBare = await bookmark_service.delete(session, bookmark)

    return StatusResponse()
