import asyncio

import asyncpg.exceptions

from app.database import get_pool
from app.queries.user import User
# from database import Database

async def create_tables():
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS users
                (
                    id         SERIAL PRIMARY KEY,
                    name       VARCHAR(255) NOT NULL,
                    username   VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
                '''
            )
            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS messages
                (
                    id         SERIAL PRIMARY KEY,
                    content    TEXT NOT NULL,
                    user_id    integer REFERENCES users (id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
                '''
            )
        except Exception as e:
            print(e)


async def main():
    # await create_tables()
    try:
        await User(name="vladik", username="dada").save()
    except asyncpg.exceptions.UniqueViolationError as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
