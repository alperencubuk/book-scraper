from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Book Scraper"
    VERSION: str = "1.0.0"

    API_KEY: str = "apikey"
    API_KEY_HEADER: str = "Authorization"

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_URI: str | None = None

    @model_validator(mode="after")
    def validator(cls, values: "Settings") -> "Settings":
        values.MONGO_URI = (
            "mongodb://"
            f"{values.MONGO_INITDB_ROOT_USERNAME}:"
            f"{values.MONGO_INITDB_ROOT_PASSWORD}@"
            f"{values.MONGO_HOST}:{values.MONGO_PORT}"
        )
        return values


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
