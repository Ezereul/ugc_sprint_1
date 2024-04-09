from flask import current_app


def send_message(topic, key, value):
    producer = current_app.producer

    producer.send(
        topic=topic,
        value=value,
        key=key,
    )
