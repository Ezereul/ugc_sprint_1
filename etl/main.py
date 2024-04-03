import asyncio

import msgspec
from aiokafka import AIOKafkaConsumer

from src.constants import Topics
from src.schemas import TOPIC_TO_SCHEMA
from src.config import settings


async def start_consumer(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=settings.kafka_url,
        value_deserializer=lambda value: msgspec.json.decode(value, type=TOPIC_TO_SCHEMA[topic])
    )
    try:
        await consumer.start()
        async for msg in consumer:
            print("Consumer got new message: %s" % msg)
    finally:
        await consumer.stop()


async def main():
    consumers_coros = [start_consumer(topic) for topic in Topics]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(coro) for coro in consumers_coros]


if __name__ == '__main__':
    asyncio.run(main())
