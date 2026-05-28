import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.environ["DATABASE_URL"]
APP_ENV: str = os.getenv("APP_ENV", "DEVELOPMENT")