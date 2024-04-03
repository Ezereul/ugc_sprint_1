import asyncio

import msgspec
from aiokafka import AIOKafkaConsumer

from src.constants import Topics
from src.schemas import TOPIC_TO_SCHEMA

BOOTSTRAP_SERVER = 'localhost:9094'
CONSUMER_TIMEOUT_MS = 10 * 1000


async def start_consumer(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVER,
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
