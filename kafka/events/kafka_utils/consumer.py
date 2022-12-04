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
            async for msg in self.consumer:
                self.logger.info(f'started consume message: {msg.value}')
                await self._consume(msg)
        finally:
            self.logger.info('stopping')
            await self.consumer.stop()
            self.logger.info('consume stopped')

    async def stop(self, exception: Exception = None):
        if self.consumer is not None:
            await self.consumer.stop()

    async def _consume(self, message: ConsumerRecord):
        err_extra_info = {
            'raw_message': message.value,
            'topic': message.topic,
            'partition': message.partition,
            'offset': message.offset
        }
        self.logger.debug(f'Consumed on: topic={message.topic}, partition={message.partition}')

        try:
            record = self.InputModel(**message.value)
            await self.process(record)
        except ValidationError:
            self.logger.info('Unable to parse kafka message', extra=err_extra_info)
            await asyncio.sleep(self.on_error_wait)

    @abstractmethod
    async def process(self, message: InputModel) -> InputModel:
        """
        Обработка полученного сообщения.

        Выполняется после сериализации к указанному виду сообщения
        """
        pass

    @abstractmethod
    async def on_startup(self):
        pass
