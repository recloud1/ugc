import datetime
import uuid

from events.constants import Events
from pydantic import BaseModel


class EventMessage(BaseModel):
    payload: dict

    class Config:
        use_enum_values = True


class EventMessageBare(EventMessage):
    id: uuid.UUID
    name: Events
    created_by: uuid.UUID
    timestamp: datetime.datetime

    class Config(EventMessage.Config):
        orm_mode = True
