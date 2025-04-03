from fastapi import APIRouter, Depends, Request

from http_client import CMCHttpClient
from dependencies import get_cmc_client

router = APIRouter(prefix='/cryptocurrency',
                   tags=['Информация о криптовалютах'])


@router.get(
    "",
    summary="Получить все криптовалюты",
)
async def get_cryptocurrencies(
    client: CMCHttpClient = Depends(get_cmc_client),
):
    """
    Получить список всех криптовалют.

    Args:
        client (CMCHttpClient): HTTP-клиент для работы с API CoinMarketCap.

    Returns:
        list: Список всех криптовалют.
    """
    return await client.get_listings()


@router.get(
    "/{currency_id}",
    summary="Получить криптовалюту по id",
)
async def get_currency(
    currency_id: int,
    client: CMCHttpClient = Depends(get_cmc_client),
):
    """
    Получить информацию о криптовалюте по ее идентификатору.

    Args:
        currency_id (int): Идентификатор криптовалюты.
        client (CMCHttpClient): HTTP-клиент для работы с API CoinMarketCap.

    Returns:
        dict: Информация о криптовалюте.
    """
    return await client.get_currency(currency_id)
