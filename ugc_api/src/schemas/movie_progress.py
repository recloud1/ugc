import datetime
import uuid

from pydantic import BaseModel, Field
from schemas.event_messages import EventMessage, EventMessageBare


class MovieProgressTimestamp(BaseModel):
    user_id: uuid.UUID = Field(
        ..., description="Идентификатор пользователя, который просматривает фильм"
    )
    movie_id: uuid.UUID = Field(
        ..., description="Идентификатор фильма, который просматривает пользователь"
    )
    timestamp: datetime.time = Field(
        ..., description="Временная отметка остановки фильма"
    )


class MovieProgressTimestampMessage(EventMessage):
    payload: MovieProgressTimestamp


class MovieProgressTimestampMessageBare(
    EventMessageBare, MovieProgressTimestampMessage
):
    pass
