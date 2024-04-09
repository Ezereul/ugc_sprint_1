from kafka.producer.future import RecordMetadata
from flask import current_app


def send_message(topic: str, key: str, value) -> RecordMetadata:
    producer = current_app.producer

    return producer.send(topic=topic, value=value, key=key)
