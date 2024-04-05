import asyncio
from aiohttp import ClientSession
from aiochclient import ChClient

hosts = [
    ('localhost', 8123, 'shard1', 'replica_1'),
    ('localhost', 8124, 'shard1', 'replica_2'),
    ('localhost', 8125, 'shard2', 'replica_1'),
    ('localhost', 8126, 'shard2', 'replica_2'),
]

async def create_tables(session, host, port, shard, replica):
    client = ChClient(session, url=f"http://{host}:{port}")

    database_name = "shard" if "replica_1" in replica else "replica"

    await client.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

    tables_config = [
        ('clicks', 'user_id', 'user_id'),
        ('views', 'time', 'time'),
        ('pages', 'duration', 'duration'),
        ('custom_events', 'time', 'time'),
    ]

    for table_name, partition_key, order_key in tables_config:
        zookeeper_path = f"/clickhouse/{shard}/{table_name}"

        await client.execute(f"""
        CREATE TABLE IF NOT EXISTS {database_name}.{table_name}
        (
            user_id UUID,
            time DateTime,
            {"obj_id String," if table_name == "clicks" else ""}
            {"film_id UUID," if table_name == "views" else ""}
            {"url String," if table_name == "pages" else ""}
            {"duration Float32," if table_name == "pages" else ""}
            {"timecode String," if table_name == "views" else ""}
            {"information String," if table_name == "custom_events" else ""}
        ) Engine=ReplicatedMergeTree('{zookeeper_path}', '{replica}')
        PARTITION BY toYYYYMM(time)
        ORDER BY ({order_key})
        """)

        if 'replica_1' in replica:
            await client.execute(f"""
            CREATE TABLE IF NOT EXISTS default.{table_name}_distributed AS {database_name}.{table_name}
            ENGINE = Distributed('company_cluster', '', '{table_name}', cityHash64({order_key}))
            """)
            print(f"Distributed tables created on {host}:{port}")

async def main():
    async with ClientSession() as session:
        tasks = [create_tables(session, *host_info) for host_info in hosts]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
