import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")
TELEGRAM_API = os.getenv("TELEGRAM_API")
PROJECT_NAME = os.getenv("PROJECT_NAME")
EMAIL = os.getenv("EMAIL")
