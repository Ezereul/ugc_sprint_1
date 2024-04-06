import asyncio
import json

from aiohttp import ClientSession
from aiochclient import ChClient

from src.core.config import settings, logger
from src.core.constants import Topics
from src.components.consumer import get_kafka_consumer
from src.schemas import Click, Page, CustomEvent, View


async def load_stub(topic: str, values: list[Click | Page| CustomEvent | View]):
    rows_to_insert = []
    for event in values:
        row = [event.user_id, event.time]

        if topic == Topics.CLICKS:
            row.extend([event.obj_id])
        elif topic == Topics.VIEWS:
            row.extend([event.film_id, event.timecode.strftime("%H:%M:%S.%f")])
        elif topic == Topics.PAGES:
            row.extend([event.url, event.duration])
        elif topic == Topics.CUSTOM_EVENTS:
            row.extend([json.dumps(event.information)])

        rows_to_insert.append(tuple(row))
    print(rows_to_insert)


    async with ClientSession() as session:
        client = ChClient(session, url=f"http://{settings.clickhouse_1_host}:{settings.clickhouse_1_port}")
        await client.execute(
            f'INSERT INTO default.{topic}_distributed VALUES',
            *rows_to_insert,
        )


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

                try:
                    await load_stub(topic, values)
                    await consumer.commit()
                except Exception:
                    logger.exception("Error while loading in Clickhouse")

            else:
                logger.info('"%s", records (%s/%s).' % (topic, new_records_count, settings.consumer_min_poll_records))
                await asyncio.sleep(settings.consumer_timeout_ms / 1000)


async def main():
    consumers_coros = [start_consumer(str(topic)) for topic in Topics]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(coro) for coro in consumers_coros]


if __name__ == '__main__':
    asyncio.run(main())
