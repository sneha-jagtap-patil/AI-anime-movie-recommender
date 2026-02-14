import os
from dotenv import load_dotenv

load_dotenv()

GROQL_API_KEY = os.getenv("GROQL_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "groq:qwen/qwen3-32b"
