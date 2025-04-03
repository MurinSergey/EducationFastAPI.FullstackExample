from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Класс Config представляет конфигурацию приложения.

    Атрибуты:
    CMC_API_KEY (str): Ключ API для CoinMarketCap.
    CMC_BASE_URL (str): Базовый URL для CoinMarketCap.
    """
    model_config = SettingsConfigDict(
        env_file='backend\security\.env', env_file_encoding='utf-8')
    CMC_API_KEY: str
    CMC_BASE_URL: str


settings = Config()
