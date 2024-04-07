import msgspec
from aiokafka import AIOKafkaConsumer

from src.config import settings
from src.schemas import TOPIC_TO_SCHEMA


def _msgspec_deserializer(binary_str: bytes, schema: type[msgspec.Struct]):
    return msgspec.json.decode(binary_str, type=schema)


def get_kafka_consumer(topic: str) -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        topic,
        bootstrap_servers=settings.kafka_url,
        value_deserializer=lambda value: _msgspec_deserializer(value, TOPIC_TO_SCHEMA[topic]),
        enable_auto_commit=False,
        group_id=topic,
        auto_offset_reset='earliest',
    )
