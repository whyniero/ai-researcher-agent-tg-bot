import asyncio

import asyncpg
import os
from dotenv import load_dotenv
import logging

load_dotenv()

DB_URL = os.getenv("DB_URL")

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        while True:
            try:
                _pool = await asyncpg.create_pool(DB_URL)
                logging.info("Connection to db successful!")
                break
            except (asyncpg.exceptions.ClientCannotConnectError,
                    asyncpg.exceptions.PostgresConnectionError,
                    ConnectionError,
                    OSError,
                    ) as e:
                logging.warning("Connection refused...")
                await asyncio.sleep(3)
    return _pool


class Database:
    def __init__(self, db_url=DB_URL):
        self.DB_URL = db_url
