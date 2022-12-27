from core.config import envs
from internal.mongo_crud.base import BaseCrud
from internal.mongo_crud.constants import Collections

bookmark_service = BaseCrud(
    db_name=envs.mongo.name, collection_name=Collections.bookmarks
)
