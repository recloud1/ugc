from motor.motor_asyncio import AsyncIOMotorClient

from core.config import envs
from internal.mongo_crud.base import BaseMongoCrud
from internal.mongo_crud.constants import Collections


class MovieLikeCrud(BaseMongoCrud):
    async def count(
        self, session: AsyncIOMotorClient, movie_id: str
    ) -> tuple[int, int]:
        _, coll = self._get_db(session)
        total_count = await coll.count_documents({"movie_id": movie_id})
        likes = await coll.count_documents(
            {"$and": [{"movie_id": movie_id}, {"value": {"$eq": 10}}]}
        )
        dislikes = total_count - likes

        return likes, dislikes


movie_like_crud = MovieLikeCrud(
    db_name=envs.mongo.name, collection_name=Collections.likes
)
