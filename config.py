import os
from dotenv import load_dotenv


load_dotenv(override=True)

#####################
# LLM
#####################
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "hoge")
OPENAI_CHAT_ENDPOINT = os.getenv("OPENAI_CHAT_ENDPOINT", "fuga")

#####################
# OpenSearch
#####################
INDEX_NAME = "trial_index"
