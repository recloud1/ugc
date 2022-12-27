from core.config import envs
from internal.mongo_crud.base import BaseCrud
from internal.mongo_crud.constants import Collections
from schemas.reviews import ReviewBare, ReviewList

review_service = BaseCrud(db_name=envs.mongo.name, collection_name=Collections.reviews)
