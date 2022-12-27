from schemas.base import Model


class ReviewUpdate(Model):
    value: str


class ReviewCreate(ReviewUpdate):
    movie_id: str


class ReviewBare(ReviewUpdate):
    id: str
    user_id: str


class ReviewList(Model):
    data: list[ReviewBare]
