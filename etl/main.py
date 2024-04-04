import asyncio
import logging

import msgspec
from aiokafka import AIOKafkaConsumer
from aiokafka.structs import TopicPartition

from src.config import settings
from src.constants import Topics
from src.schemas import TOPIC_TO_SCHEMA

logger = logging.getLogger(__name__)
logging.basicConfig(format=settings.log_format, level=settings.log_level)


async def load_stub(topic: str, msgs: list):
    logger.critical("CLICKHOUSE \"%s\" got new messages. Msgs=%s." % (topic, len(msgs)))


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
        logger.info("Consumer for topic \"%s\" was successfully started." % topic)

        t_partitions = [TopicPartition(topic, partition) for partition in consumer.partitions_for_topic(topic)]

        while True:
            last_offsets = await consumer.end_offsets(t_partitions)
            commit_offsets = await consumer.seek_to_committed(*t_partitions)

            new_records_count = sum(offset_last - (offset_commit or 0)
                                    for offset_last, offset_commit
                                    in zip(last_offsets.values(), commit_offsets.values()))

            if new_records_count < settings.consumer_min_batch_size:
                logger.info('topic="%s", records (%s/%s)' %
                            (topic, new_records_count, settings.consumer_min_batch_size))
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)
                continue

            result = await consumer.getmany(timeout_ms=settings.consumer_timeout_ms)
            values = [record.value for sublist in result.values() for record in sublist]

            await load_stub(topic, values)
            await consumer.commit()

    finally:
        await consumer.stop()


async def main():
    consumers_coros = [start_consumer(str(topic)) for topic in Topics]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(coro) for coro in consumers_coros]


if __name__ == '__main__':
    asyncio.run(main())
