from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
    SELLERS_ENDPOINT: HttpUrl
    CLIENTS_ENDPOINT: HttpUrl
    PRODUCTS_ENDPOINT: HttpUrl
    SALES_ENDPOINT: HttpUrl
    AMQP_URL: str
    EXCHANGE_SELLERS: str
    QUEUE_SELLERS: str
    PREFETCH_COUNT: int | None = None
