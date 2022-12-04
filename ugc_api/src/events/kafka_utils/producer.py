import logging
from abc import abstractmethod
from typing import Any, Type, TypeVar

import aiomisc
import orjson
from aiokafka import AIOKafkaProducer
from pydantic import BaseModel, ValidationError

from events.constants import Events, get_topic_name
from events.kafka_utils.config import KafkaConfig

OutputType = TypeVar('OutputType', bound=BaseModel)


class KafkaProducer(aiomisc.Service):
    OutputModel: Type[OutputType] = None
    on_error_wait = 0.2

    def __init__(self, connection_config: KafkaConfig, **kwargs):
        super().__init__(**kwargs)
        self.kafka_config = connection_config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.producer: AIOKafkaProducer | None = None

        if not self.OutputModel:
            raise TypeError('You should specify OutputModel type')

    async def start(self, trigger_start: bool = True) -> None:
        if self.producer is None:
            self.producer = self._create_producer()
        else:
            raise Exception('Only single run allowed for producer')

        await self.producer.start()

        await self.on_startup()
        self.logger.info(f'started up {self.kafka_config.input_topic}')

        if trigger_start:
            self.start_event.set()

    async def stop(self, exception: Exception = None) -> None:
        if self.producer is not None:
            await self.producer.stop()

    @abstractmethod
    async def on_startup(self):
        """Необязательный к реализации хук, который выполняется до запуска producer'а"""

    async def send_message(self, event: Events, message: OutputModel):
        """
        Отправка сообщения в топик.

        По-умолчанию принимается объект, условленного в рамках producer'a типа, однако,
        можно передать объект, который будет принудительно сериализован в OutputModel.
        """
        if not isinstance(message, self.OutputModel):
            try:
                message = self.pack(message)
            except ValidationError as e:
                raise TypeError(
                    f'Failed to pack message {type(message)} to {self.OutputModel}'
                ) from e

        await self.producer.send(get_topic_name(event), message.dict())

    def pack(self, data: Any) -> OutputModel:
        """
        Функция по упаковке данных в формат сообщения для отправки в топик.

        Функция автоматически вызывается, если при отправке сообщения не был
         передан объект соответствующего типа
        """
        raise NotImplemented('Packing data is not implemented')

    def _create_producer(self) -> AIOKafkaProducer:
        return AIOKafkaProducer(
            client_id=self.kafka_config.group_id,
            loop=self.loop,
            bootstrap_servers=self.kafka_config.bootstrap_servers,
            value_serializer=orjson.dumps
        )
