from schemas.base import Model


class CommonLike(Model):
    user_id: str


class MovieLikeCreate(CommonLike):
    movie_id: str


class MovieLikeBare(MovieLikeCreate):
    id: str


class MovieLikeCount(Model):
    movie_id: str
    likes: int
    dislikes: int
