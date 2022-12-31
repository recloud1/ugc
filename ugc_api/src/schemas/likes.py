from schemas.base import Model


class MovieLikeCreate(Model):
    movie_id: str
    value: int


class MovieLikeBare(MovieLikeCreate):
    id: str
    user_id: str


class MovieLikeCount(Model):
    movie_id: str
    likes: int
    dislikes: int
