import os

import openai
from openai import OpenAI
from pyexpat.errors import messages


class LLM:
    def __init__(self):
        self.openai = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_answer(self):
        self.openai.responses.create(
            model="gemma3:4b",
            instructions="You are search agent",
            input="What is your name?",
            temperature=0.2,
        )
