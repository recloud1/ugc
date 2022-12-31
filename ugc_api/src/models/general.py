from sqlalchemy import Column, DateTime, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from models import Base
from utils.time import now


class Event(Base):
    __tablename__ = "stream_events"
    __table_args__ = {"schema": "general"}

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    name = Column(Text)
    payload = Column(JSONB)
    timestamp = Column(DateTime, default=now)
    sent_at = Column(DateTime)

    created_at = Column(DateTime, default=now)
    created_by = Column(UUID(as_uuid=True), nullable=False)
