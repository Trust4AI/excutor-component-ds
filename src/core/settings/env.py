from dotenv import load_dotenv
import os


class Env:
    def __init__(self):
        load_dotenv()

    def get(self, key: str):
        return os.getenv(key)


env = Env()
