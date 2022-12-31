from core.config import envs
from internal.mongo_crud.base import BaseMongoCrud
from internal.mongo_crud.constants import Collections

review_service = BaseMongoCrud(
    db_name=envs.mongo.name, collection_name=Collections.reviews
)
