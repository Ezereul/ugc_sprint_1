import asyncio

from aiochclient import ChClient
from aiohttp import ClientSession


async def create_tables(session: ClientSession):
    pass


async def main():
    async with ClientSession() as session:
        client = ChClient(session)
        await create_tables(session)
        # result = await client.execute("CREATE DATABASE IF NOT EXISTS users ON CLUSTER company_cluster")


if __name__ == '__main__':
    asyncio.run(main())
