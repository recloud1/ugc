import fastapi
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db_session import get_db_session, get_mongo_session

db_session: AsyncSession = fastapi.Depends(get_db_session)

mongo_session: AsyncIOMotorClient = fastapi.Depends(get_mongo_session)
