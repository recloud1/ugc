import datetime
import uuid

from pydantic import BaseModel

from events.constants import Events


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


class MoviesProgress(BaseModel):
    id: str
    user_id: str
    movie_id: str
    movie_progress_time: int
    created_at: int