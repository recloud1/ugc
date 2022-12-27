import logging
from typing import Any, Iterable

import aiomisc
from aiomisc.service.periodic import PeriodicService
from core.config import envs
from events.constants import Events
from events.kafka_utils.config import KafkaConfig
from events.kafka_utils.producer import KafkaProducer
from models.general import Event
from schemas.event_messages import EventMessageBare
from sqlalchemy import select
from utils.db_session import db_session_manager
from utils.time import now


class EventKafkaProducer(KafkaProducer):
    OutputModel = EventMessageBare

    async def on_startup(self):
        pass


class BatchEventStreamer(PeriodicService):
    logger = logging.getLogger("batch-event-streamer")

    def __init__(
        self, event_producer: EventKafkaProducer, batch_size: int = 200, *args, **kwargs
    ):
        self.event_producer = event_producer
        self.batch_size = batch_size

        super().__init__(**kwargs)

    async def callback(self) -> Any:
        async with db_session_manager() as session:
            query = (
                select(Event)
                .where(Event.sent_at == None)
                .order_by(Event.timestamp)
                .limit(self.batch_size)
            )
            values: Iterable[Event] = await session.scalars(query)

            for event in values:
                await self.event_producer.send_message(
                    Events(event.name),
                    EventMessageBare(
                        id=str(event.id),
                        name=Events(event.name),
                        payload=event.payload,
                        timestamp=event.timestamp,
                        created_by=str(event.created_by),
                    ),
                )
                self.logger.info(f"event: {event.id} sent")
                event.sent_at = now()


if __name__ == "__main__":
    connection_config = KafkaConfig(
        input_topic=None,
        group_id=envs.kafka.group_id,
        bootstrap_servers=envs.kafka.bootstrap_servers,
    )
    event_producer = EventKafkaProducer(connection_config)

    with aiomisc.entrypoint(
        event_producer,
        BatchEventStreamer(event_producer, interval=5),
        log_level=logging.INFO,
    ) as loop:
        loop.run_forever()
