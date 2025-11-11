import asyncpg
import os
from dotenv import load_dotenv
import logging

load_dotenv()

DB_URL = os.getenv("DB_URL")


async def get_pool():
    while True:
        try:
            pool = await asyncpg.create_pool(DB_URL)
            logging.info("Connection to db successful!")
            return pool
        except Exception as e:
            logging.warn("Connection refused...")


class Database:
    def __init__(self, db_url=DB_URL):
        self.DB_URL = db_url
