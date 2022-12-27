from schemas.base import Model


class BookmarkCreate(Model):
    movie_id: str


class BookmarkBare(BookmarkCreate):
    id: str
    user_id: str


class BookmarkList(Model):
    data: list[BookmarkBare]
