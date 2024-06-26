import os
from dotenv import load_dotenv


load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "hoge")
OPENAI_CHAT_ENDPOINT = os.getenv("OPENAI_CHAT_ENDPOINT", "fuga")
