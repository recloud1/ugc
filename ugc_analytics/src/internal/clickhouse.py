from abc import ABC, abstractmethod

from clickhouse_driver import Client
from core.config import Clickhouse


class ClickhouseService(ABC):
    @abstractmethod
    def table(self) -> dict:
        pass

    @abstractmethod
    def create_table(self) -> None:
        pass

    @abstractmethod
    def insert(self, values: list[dict]) -> int:
        pass


class MoviesProgressService(ClickhouseService):
    def __init__(self, config: Clickhouse, connect: Client | None = None):
        self.config = config
        self._adapter = self.create_connect(connect)

    def create_connect(self, connect: Client | None = None):
        if connect is None:
            connect = Client(host=self.config.host, port=self.config.host)

        return connect

    def table(self) -> dict:
        return {
            'id': 'String',
            'user_id': 'String',
            'movie_id': 'String',
            'movie_progress_time': 'Int64',
            'created_at': 'Int64'
        }

    def source(self) -> str:
        return f'{self.config.base}.{self.config.table}'

    def create_table(self) -> None:
        table_args = ', '.join([f'{key} {value}' for key, value in self.table().items()])
        self._adapter.execute(
            f' CREATE TABLE IF NOT EXISTS {self.source()} ({table_args}) Engine=MergeTree() ORDER BY id'
        )

    def insert(self, values: list[dict]) -> int:
        table_args = ', '.join([key for key in self.table().keys()])

        inserted_rows = self._adapter.execute(
            f'INSERT INTO {self.source()} ({table_args}) VALUES',
            params=values
        )

        return inserted_rows
