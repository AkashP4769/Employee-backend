# import os
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL: str = os.environ["DATABASE_URL"]
# APP_ENV: str = os.getenv("APP_ENV", "DEVELOPMENT")

from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    database_url:   str
    app_env:        str = "development"
    debug:          bool = False

    model_config =  SettingsConfigDict(
        env_file=".env"
    )

setting = Setting()