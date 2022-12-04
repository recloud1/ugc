from aiomisc import Service
from abc import abstractmethod
from typing import TypeVar, Type

from pydantic import BaseModel, ValidationError
import asyncio
import logging
import orjson
from aiokafka import AIOKafkaConsumer, ConsumerRecord

from events.kafka_utils.config import KafkaConfig

InputType = TypeVar('InputType', bound=BaseModel)


class KafkaConsumer(Service):
    InputModel: Type[InputType] = None

    on_error_wait = 0.2

    def __init__(self, connection_config: KafkaConfig, from_topic_begin: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.kafka_config = connection_config

        self.logger = logging.getLogger(self.__class__.__name__)
        self.consumer: AIOKafkaConsumer | None = None
        self.from_topic_begin = from_topic_begin

        if not self.InputModel:
            raise TypeError('You should specify Input Model')

        if not self.kafka_config.input_topic:
            raise ValueError('Kafka input topic should be specified in config')

    def _create_consumer(self) -> AIOKafkaConsumer:
        consumer = AIOKafkaConsumer(
            self.kafka_config.input_topic,
            loop=self.loop,
            bootstrap_servers=self.kafka_config.bootstrap_servers,
            group_id=self.kafka_config.group_id,
            value_deserializer=orjson.loads,
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )

        return consumer

    async def start(self, trigger_start: bool = True):
        if self.consumer is None:
            self.consumer = self._create_consumer()
        else:
            raise Exception('Only single run is allowed for consumer')

        await self.on_startup()
        self.logger.info(f'Started up {self.kafka_config.input_topic}')

        if trigger_start:
            self.start_event.set()

        await self.consumer.start()
        try:
            messages = []
            async for msg in self.consumer:
                messages.append(msg)

            await self._consume(messages)
            await self.consumer.commit()
        finally:
            self.logger.info('stopping')
            await self.consumer.stop()
            self.logger.info('consume stopped')

    async def stop(self, exception: Exception = None):
        if self.consumer is not None:
            await self.consumer.stop()

    async def _consume(self, messages: list[ConsumerRecord]):
        try:
            records = [self.InputModel(**message.value) for message in messages]
            await self.process(records)
        except ValidationError:
            await asyncio.sleep(self.on_error_wait)

    @abstractmethod
    async def process(self, message: list[InputModel]) -> None:
        """
        Обработка полученных сообщений.

        Выполняется после сериализации к указанному виду сообщения
        """
        pass

    @abstractmethod
    async def on_startup(self):
        pass
