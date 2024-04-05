import asyncio
from src.core.config import settings, logger
from src.core.constants import Topics
from src.components.consumer import get_kafka_consumer


async def load_stub(topic: str, msgs: list):
    logger.critical("CLICKHOUSE \"%s\" got new messages. Msgs=%s." % (topic, msgs))


async def start_consumer(topic: str):
    async with get_kafka_consumer(topic) as consumer:
        t_partitions = consumer.assignment()

        while True:
            last_offsets = await consumer.end_offsets(t_partitions)
            commit_offsets = await consumer.seek_to_committed(*t_partitions)

            new_records_count = sum(last_offsets.values()) - sum(filter(bool, commit_offsets.values()))

            if new_records_count >= settings.consumer_min_poll_records:
                result = await consumer.getmany(timeout_ms=settings.consumer_timeout_ms)
                values = [record.value for sublist in result.values() for record in sublist]

                await load_stub(topic, values)  # загрузка данных; добавлю try-except, commit будет только при успешной
                await consumer.commit()

            else:
                logger.info('"%s", records (%s/%s).' % (topic, new_records_count, settings.consumer_min_poll_records))
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)


async def main():
    consumers_coros = [start_consumer(str(topic)) for topic in Topics]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(coro) for coro in consumers_coros]


if __name__ == '__main__':
    asyncio.run(main())
