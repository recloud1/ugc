import logging

import aiomisc
from core.config import envs
from events.kafka_utils.config import KafkaConfig
from events.kafka_utils.consumer import KafkaConsumer
from events.messages.base import EventMessageBare
from internal.clickhouse import ClickhouseService, MoviesProgressService


class EventKafkaConsumer(KafkaConsumer):
    InputModel = EventMessageBare

    def __init__(self, connection_config: KafkaConfig, clickhouse: ClickhouseService, **kwargs):
        self.clickhouse = clickhouse
        super().__init__(connection_config, **kwargs)

    async def process(self, messages: list[InputModel]) -> None:
        result_models = [dict(
            id=message.id,
            user_id=message.created_by,
            movie_id=message.payload.get('movie_id'),
            movie_progress_time=message.payload.get('movie_progress_time'),
            created_at=message.payload.get('created_at')
        ) for message in messages]

        self.clickhouse.insert(result_models)

    async def on_startup(self):
        self.clickhouse.create_table()


if __name__ == '__main__':
    kafka_config = KafkaConfig(
        input_topic=envs.kafka.topic,
        group_id=envs.kafka.group_id,
        bootstrap_servers=envs.kafka.bootstrap_servers
    )

    clickhouse_service = MoviesProgressService(config=envs.clickhouse)

    event_consumer = EventKafkaConsumer(kafka_config, clickhouse_service)

    with aiomisc.entrypoint(event_consumer, log_level=logging.INFO) as loop:
        loop.run_forever()
