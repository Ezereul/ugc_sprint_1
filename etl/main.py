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
        logger.debug("Consumer for topic \"%s\" was started successfully." % topic)

        while True:
            topic_msgs: list[type[BaseEvent]] = []
            start_topic_partition_offset: dict[TopicPartition, int] = {}
            await consumer.seek_to_committed()
            result = await consumer.getmany(timeout_ms=settings.consumer_timeout_ms)

            if not result:
                logger.info('Topic \"%s\" has no records.' % topic)
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)
                continue

            for partition, partition_msgs in result.items():
                start_topic_partition_offset[partition] = partition_msgs[0].offset
                topic_msgs.extend([msg.value for msg in partition_msgs])

            logger.debug(start_topic_partition_offset)

            if len(topic_msgs) < settings.consumer_min_batch_size:
                logger.info('Topic \"%s\" is sleeping. Found %s records.' % (topic, len(topic_msgs)))
                await consumer.commit(start_topic_partition_offset)
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)
                continue
            else:
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
