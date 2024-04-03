import asyncio
from enum import StrEnum

from aiokafka import AIOKafkaConsumer

BOOTSTRAP_SERVER = 'localhost:9094'
CONSUMER_TIMEOUT_MS = 10 * 1000


class Topics(StrEnum):
    CLICKS = 'clicks'
    CUSTOM_EVENTS = 'custom_events'
    VIEWS = 'views'
    PAGES = 'pages'


async def start_consumer(topic):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=BOOTSTRAP_SERVER)
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
