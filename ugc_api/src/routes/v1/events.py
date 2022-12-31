import datetime

import fastapi
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.auth import user_authorized
from events.constants import Events
from internal.events import event_crud
from schemas.auth import UserInfo
from schemas.event_messages import EventMessage, EventMessageBare
from utils.db_session import get_db_session

events = fastapi.APIRouter()


@events.post(
    "/",
    response_model=EventMessageBare,
    summary="Сохранения события",
    description="Производиться сохранение пользовательского события в базу данных",
)
async def save_event_message(
    data: EventMessage,
    name: Events = Query(...),
    session: AsyncSession = Depends(get_db_session),
    author: UserInfo = Depends(user_authorized),
) -> EventMessageBare:
    """
    Сохранение пользовательского события
    """

    event = await event_crud.create(
        session,
        data,
        name=name,
        timestamp=datetime.datetime.utcnow(),
        created_by=author.id,
    )

    return EventMessageBare.from_orm(event)
