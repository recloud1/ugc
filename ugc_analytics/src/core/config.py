from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = '.env'


class Clickhouse(Settings):
    host: str
    port: int
    base: str
    table: str

    class Config(Settings.Config):
        env_prefix = 'CLICKHOUSE_'


class Kafka(Settings):
    bootstrap_servers: str
    topic: str
    group_id: str

    class Config(Settings.Config):
        env_prefix = 'KAFKA_'


class Envs(Settings):
    clickhouse: Clickhouse = Clickhouse()
    kafka: Kafka = Kafka()


envs = Envs()
