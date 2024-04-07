def send_message(topic, key, value):
    from flask_app.app import producer

    producer.send(
        topic=topic,
        value=value,
        key=key,
    )
