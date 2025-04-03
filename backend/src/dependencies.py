from fastapi import Request
from http_client import CMCHttpClient


async def get_cmc_client(request: Request) -> CMCHttpClient:
    """
    Возвращает экземпляр CMCHttpClient из состояния приложения.

    Args:
    request (Request): Объект запроса.

    Returns:
    CMCHttpClient: Экземпляр CMCHttpClient.
    """
    return request.app.state.cmc_client