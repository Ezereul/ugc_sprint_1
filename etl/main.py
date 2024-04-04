import asyncio
import logging

import msgspec
from aiokafka import AIOKafkaConsumer
from aiokafka.structs import TopicPartition

from src.config import settings
from src.constants import Topics
from src.schemas import TOPIC_TO_SCHEMA, BaseEvent

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

        while True:
            topic_msgs: list[type[BaseEvent]] = []
            backup_offsets: dict[TopicPartition, int] = {}
            await consumer.seek_to_committed()

            result = await consumer.getmany(timeout_ms=settings.consumer_timeout_ms)

            if not result:
                logger.info('Topic \"%s\" has 0 records.' % topic)
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)
                continue

            for partition, partition_msgs in result.items():
                backup_offsets[partition] = partition_msgs[0].offset
                topic_msgs.extend([msg.value for msg in partition_msgs])

            logger.debug(backup_offsets)

            if len(topic_msgs) < settings.consumer_min_batch_size:
                logger.info('Topic \"%s\" has not enough records (%s/%s). Partitions count: %s.' %
                            (topic, len(topic_msgs), settings.consumer_min_batch_size, len(backup_offsets)))
                await consumer.commit(backup_offsets)
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)
                continue

            await load_stub(topic, topic_msgs)
            await consumer.commit()

    finally:
        await consumer.stop()


async def main():
    consumers_coros = [start_consumer(str(topic)) for topic in Topics]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(coro) for coro in consumers_coros]


if __name__ == '__main__':
    asyncio.run(main())
