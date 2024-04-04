import asyncio

import msgspec
from aiokafka import AIOKafkaConsumer

from src.config import settings
from src.constants import Topics
from src.schemas import TOPIC_TO_SCHEMA


async def start_consumer(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=settings.kafka_url,
        value_deserializer=lambda value: msgspec.json.decode(value, type=TOPIC_TO_SCHEMA[topic]),
        enable_auto_commit=False,
        group_id=topic,
        auto_offset_reset='earliest',
    )

    try:
        await consumer.start()

        print("Consumer for topic \"%s\" was started successfully." % topic)
        while True:
            topic_msgs = []
            topic_partitions = {}
            await consumer.seek_to_committed()
            result = await consumer.getmany(timeout_ms=settings.consumer_timeout_ms)

            if not result:
                print('Topic \"%s\" has no result.' % topic)
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)
                continue

            for partition, partition_msgs in result.items():
                topic_partitions[partition] = partition_msgs[0].offset
                topic_msgs.extend([msg.value for msg in partition_msgs])

            if topic_msgs:
                print(result)
                print(topic_msgs)
                print(topic_partitions)

            if len(topic_msgs) < settings.consumer_min_batch_size:
                print('Topic \"%s\" is sleeping. Found %s records.' % (topic, len(topic_msgs)))
                await consumer.commit(topic_partitions)
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)
                continue
            else:
                print("CLICKHOUSE \"%s\" got new messages. Msgs=%s." % (topic, len(topic_msgs)))
                await consumer.commit()

    finally:
        await consumer.stop()


async def main():
    consumers_coros = [start_consumer(str(topic)) for topic in Topics]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(coro) for coro in consumers_coros]


if __name__ == '__main__':
    asyncio.run(main())
