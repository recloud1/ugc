import datetime
import uuid
from typing import TypeVar

from events.constants import Events
from pydantic import BaseModel, Field

Payload = TypeVar("Payload", bound=BaseModel)


class EventMessage(BaseModel):
    payload: Payload = Field(..., description="Информация о событии")


class EventMessageBare(EventMessage):
    id: uuid.UUID
    name: Events = Field(..., description="Тип события")
    created_by: uuid.UUID
    timestamp: datetime.datetime

    class Config(EventMessage.Config):
        orm_mode = True
        use_enum_values = True
