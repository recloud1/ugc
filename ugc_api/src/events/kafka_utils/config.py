from dataclasses import dataclass


@dataclass
class KafkaConfig:
    group_id: str | None
    bootstrap_servers: list[str] | str
    input_topic: str | None
