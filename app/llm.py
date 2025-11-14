import os

import openai
from openai import OpenAI
from pyexpat.errors import messages


class LLM:
    def __init__(self):
        self.openai = OpenAI(
            base_url="http://127.0.0.1:1234/v1",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_answer(self, query: str, instructions: str = "Ты агент, ищущий информацию в поисковом движке Google",
                        tools: list = None):
        response = self.openai.responses.create(
            model="google/gemma-3n-e4b",
            instructions=instructions,
            input=query,
            temperature=0.2,
            tools=tools
        )

        return response
