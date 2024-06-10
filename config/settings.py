from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(".env")


class Settings(BaseSettings):
    MYSQL_HOST: str = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER: str = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASS: str = os.environ.get("MYSQL_PASS")
    MYSQL_PORT: int = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_DB: str = os.environ.get("MYSQL_DB", "safe_gold")
    DATABASE_URI: str = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY")


@lru_cache
def get_settings():
    return Settings()
