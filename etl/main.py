import asyncio
from enum import StrEnum

from aiokafka import AIOKafkaConsumer

BOOTSTRAP = 'localhost:9094'


class Topics(StrEnum):
    CLICKS = 'clicks'
    CUSTOM_EVENTS = 'custom_events'
    VIEWS = 'views'
    PAGES = 'pages'


async def main():
    consumer = AIOKafkaConsumer(*Topics, bootstrap_servers=BOOTSTRAP)
    try:
        await consumer.start()
        async for msg in consumer:
            print("Consumer got new message: %s" % msg)
    finally:
        await consumer.stop()



if __name__ == '__main__':
    asyncio.run(main())
