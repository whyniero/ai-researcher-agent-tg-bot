from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.database import get_pool
from app.queries.generic import GenericBase


class BaseMessageModel(BaseModel):
    content: str
    user_id: int


class GetMessageModel(BaseMessageModel):
    id: int
    created_at: datetime
    updated_at: datetime


class Message(GenericBase):
    def __init__(self, content: str, user_id: str):
        super().__init__()
        self.content = content
        self.user_id = user_id

    async def save(self):
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                '''
                INSERT INTO messages (content, user_id)
                VALUES ($1, $2)
                ''', self.user_id, self.content)

    @staticmethod
    async def all() -> List[GetMessageModel]:
        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                '''
                SELECT *
                FROM messages
                '''
            )
            return rows

    @staticmethod
    async def update(user_id: int, content: str, message_id: int):
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                '''
                UPDATE messages
                SET content = $1
                WHERE id = $2
                  AND user_id = $3
                ''', content, message_id, user_id
            )

    # @staticmethod
    # async def _get(user_id: int):
    #             pool = await get_pool()
    #         async with pool.acquire() as conn:
    #             row = await conn.fetchrow(
    #                 '''
    #                 SELECT *
    #                 FROM messages
    #                 WHERE user_id = $1
    #                 ''', user_id)
    #             return row

    @staticmethod
    async def delete(message_id: int):
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                '''
                DELETE
                FROM messages
                WHERE id = $1
                ''', message_id)
