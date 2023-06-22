# mypy: disable-error-code="call-arg"

from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    app_name: str = "Fubar Auth Service"
    database_url: str
    jwt_secret_key: str
    api_key: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_config() -> Config:
    return Config()


config = get_config()
