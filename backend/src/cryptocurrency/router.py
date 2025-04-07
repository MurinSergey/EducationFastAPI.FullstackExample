from fastapi import APIRouter, Depends
from src.dependencies import get_cmc_client
from src.protocols import http_client as http_client_protocol

# Создаем роутер с префиксом "/cryptocurrency" и тегом "Информация о криптовалютах"
router = APIRouter(prefix='/cryptocurrency',
                   tags=['Информация о криптовалютах'])


@router.get(
    "",
    summary="Получить все криптовалюты",
)
async def get_cryptocurrencies(
    client: http_client_protocol = Depends(get_cmc_client),
):
    """
    Получает все криптовалюты.

    Args:
        client (http_client_protocol): Клиент для получения данных о криптовалютах.

    Returns:
        list: Список всех криптовалют.
    """
    return await client.get_all()


@router.get(
    "/{currency_id}",
    summary="Получить криптовалюту по id",
)
async def get_currency(
    currency_id: int,
    client: http_client_protocol = Depends(get_cmc_client),
):
    """
    Получает криптовалюту по id.

    Args:
        id (int): Идентификатор криптовалюты.
        client (http_client_protocol): Клиент для получения данных о криптовалютах.

    Returns:
        dict: Информация о криптовалюте.
    """
    return await client.get_by_id(currency_id)
