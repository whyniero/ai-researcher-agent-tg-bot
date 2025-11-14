import asyncio
import json
import os

import asyncpg.exceptions
import pandas
import pandas as pd

from app.database import get_pool
from app.google_api import GoogleSearch
from app.llm import LLM
from app.queries.user import User


# <script async src="https://cse.google.com/cse.js?cx=80d8361b4bbe24441">
# </script>
# <div class="gcse-search"></div>

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


# async def main():
# await create_tables()
# try:
#     await User(name="vladik", username="dada").save()
# except asyncpg.exceptions.UniqueViolationError as e:
#     print(e)


tools = [
    {
        "type": "function",
        "name": "web_search",
        "description": "Найди требуемые пользователем ответы на его запросы.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Запрос для поиска в Google поиске.",
                },
                "count": {
                    "type": "int",
                    "description": "Количество запрашиваемых результатов. От 1 до 1000 включительно.",
                },
            },
            "required": ["query", "count"],
        },
    },
]


def web_search(query: str, count: int):
    search_results = GoogleSearch().get_search_results(query=query, count=count)
    return search_results


if __name__ == "__main__":
    filter_web_search = ""
    results = ""
    web_search_results = None

    user_query: str = input("Поиск: ")
    input_list = [
        {"role": "user", "content": user_query}
    ]

    response = LLM().generate_answer(user_query, tools=tools)
    input_list += response.output

    for item in response.output:
        if item.type == "function_call":
            if item.name == "web_search":
                args = json.loads(item.arguments)
                web_search_results = web_search(args["query"], args["count"])

                # 4. Provide function call results to the model
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "search_results": [wsr['snippet'] for wsr in web_search_results],
                    })
                })

    prompt = ""
    # df = pandas.DataFrame(web_search_results)
    # df.to_csv("results.csv", index=False)
    for wsr in web_search_results:
        prompt += (f"Заголовок: {wsr['title']}\n"
                   f"Ссылка: {wsr['link']}\n"
                   f"Фрагмент: {wsr['snippet']}\n\n")

    filter_web_search = LLM().generate_answer(
        prompt,
        instructions="Ты фильтруешь итоговые результаты от Google Search API таким образом,"
                     "что пользователю отображаются краткие ответы (не более 2х предложений) с указанием источника."
                     "Никаких разных вариантов, строго по количеству передаваемых запросов все делай. Отвечай строго на русском языке")
    answer = filter_web_search.output[0].content[0].text

    print(answer)
