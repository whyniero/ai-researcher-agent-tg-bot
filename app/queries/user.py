from datetime import datetime

from pydantic import BaseModel

from app.database import get_pool
from app.queries.generic import GenericBase


class BaseUserModel(BaseModel):
    name: str
    username: str


class GetUserModel(BaseUserModel):
    id: int
    created_at: datetime
    updated_at: datetime


class User(GenericBase):
    def __init__(self, name: str, username: str):
        super().__init__()
        self.name = name
        self.username = username

    async def save(self):
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                '''
                INSERT INTO users (name, username)
                VALUES ($1, $2)
                ''', self.name, self.username)

    @staticmethod
    async def all():
        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                '''
                SELECT users.name, users.username
                FROM users
                '''
            )
            return rows

    @staticmethod
    async def get(user_id: int) -> GetUserModel:
        pool = await get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                '''
                SELECT *
                FROM users
                WHERE id = $1
                ''', user_id
            )
            return row

    @staticmethod
    async def update(user_id: int, name: str, username: str):
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                '''
                UPDATE users
                SET name     = $1,
                    username = $2
                WHERE id = $3
                ''', name, username, user_id
            )

    @staticmethod
    async def delete(user_id: int):
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                '''
                DELETE
                FROM users
                WHERE id = $1
                ''', user_id)
