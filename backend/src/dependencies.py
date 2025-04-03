from fastapi import Request
from src.cryptocurrency.http_client import CMCHttpClient
from src.config import settings


async def get_cmc_client(request: Request) -> CMCHttpClient:
    """
    Возвращает экземпляр CMCHttpClient из состояния приложения.

    Args:
    request (Request): Объект запроса.

    Returns:
    CMCHttpClient: Экземпляр CMCHttpClient.
    """
    return request.app.state.cmc_client

async def setup_cmc_client() -> CMCHttpClient:
    """
    Создает и возвращает экземпляр CMCHttpClient с заданными параметрами.

    Returns:
        CMCHttpClient: Экземпляр CMCHttpClient, настроенный с использованием базового URL и API ключа из настроек.
    """
    return CMCHttpClient(
        base_url=settings.CMC_BASE_URL,
        api_key=settings.CMC_API_KEY,
    )