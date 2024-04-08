from kafka.producer.future import RecordMetadata


def send_message(topic: str, key: str, value) -> RecordMetadata:
    from app import producer

    return producer.send(topic=topic, value=value, key=key)
