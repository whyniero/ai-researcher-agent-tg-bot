import os
from dotenv import load_dotenv

load_dotenv()

class GenericBase:
    def __init__(self):
        self.DB_URL = os.getenv("DB_URL")