from urllib import parse

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"


class App(Settings):
    host: str = "localhost"
    port: int = 8001
    cors_policy_enabled: bool = False
    environment: str = "LOCAL_TEST"

    class Config(Settings.Config):
        env_prefix = "APP_"


class DBConfig(Settings):
    name: str
    password: str
    host: str
    port: int
    user: str

    # async_db_conn_str: str

    @property
    def async_db_conn_str(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{parse.quote(self.password)}@{self.host}:{self.port}/{self.name}"

    class Config(Settings.Config):
        env_prefix = "DB_"


class MongoConfig(Settings):
    name: str
    password: str
    host: str
    port: int
    user: str

    @property
    def conn_str(self) -> str:
        return "mongodb://localhost:27017"

    class Config(Settings.Config):
        env_prefix = "MONGO_"


class Kafka(Settings):
    bootstrap_servers: str
    group_id: str

    class Config(Settings.Config):
        env_prefix = "KAFKA_"


class External(Settings):
    auth: str

    class Config(Settings.Config):
        env_prefix = "EXTERNAL_"


class LoggingConfig(Settings):
    sentry_url: str
    logstash_host: str
    logstash_port: int
    level: str = "DEBUG"

    class Config(Settings.Config):
        env_prefix = "LOGGING_"


class Envs(Settings):
    app: App = App()
    database: DBConfig = DBConfig()
    mongo: MongoConfig = MongoConfig()
    external: External = External()
    kafka: Kafka = Kafka()
    logging: LoggingConfig = LoggingConfig()


envs = Envs()
