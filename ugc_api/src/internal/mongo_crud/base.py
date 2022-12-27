from typing import Any, TypeVar

from core.crud.exceptions import ObjectNotExists
from internal.mongo_crud.constants import Collections
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo.results import InsertOneResult

ModelType = TypeVar("ModelType", bound=BaseModel)

BATCH_SIZE = 100


class BaseCrud:
    def __init__(
        self,
        db_name: str,
        collection_name: Collections,
    ):
        self.db_name = db_name
        self.collection_name = collection_name

    async def create(
        self, session: AsyncIOMotorClient, data: ModelType, **params: dict
    ) -> dict:
        """
        Добавление данных в коллекцию
        """
        _, coll = self._get_db(session)
        inserted: InsertOneResult = await coll.insert_one({**data.dict(), **params})

        result = await self._get(session, str(inserted.inserted_id))

        return dict(result)

    async def get(self, session: AsyncIOMotorClient, _id: str) -> dict:
        obj = await self._get(session, _id)

        return dict(obj)

    async def get_multi(
        self, session: AsyncIOMotorClient, **filter_params: dict
    ) -> list[dict]:
        _, coll = self._get_db(session)
        result = coll.find(filter_params)

        documents = []
        for doc in await result.to_list(length=BATCH_SIZE):
            documents.append(dict(doc))

        return documents

    async def update(
        self, session: AsyncIOMotorClient, _id: str, data: ModelType
    ) -> dict:
        _, coll = self._get_db(session)
        obj, _id = await self._get(session, _id)
        result = await coll.update_one({"_id": _id}, {"$set": data.dict()})

        return result

    async def delete(self, session: AsyncIOMotorClient, _id: str):
        _, coll = self._get_db(session)
        obj, _id = self._get(session, _id)
        result = coll.delete_one({"_id": _id})

        return result

    async def find(self, session: AsyncIOMotorClient, **params: dict) -> dict | None:
        _, coll = self._get_db(session)
        result = await coll.find_one({**params})

        return dict(result) if result else None

    def _get_db(self, session) -> tuple[Any, Any]:
        db = getattr(session, self.db_name)
        collection = db.get_collection(self.collection_name)

        return db, collection

    async def _get(self, session: AsyncIOMotorClient, _id: str) -> Any:
        _, coll = self._get_db(session)
        obj = await coll.find_one({"_id": _id})
        if not obj:
            raise ObjectNotExists("Объект не найден")

        return obj, _id
