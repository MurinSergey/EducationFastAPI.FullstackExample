from fastapi import APIRouter, Request

router = APIRouter(prefix='/cryptocurrency',
                   tags=['Информация о криптовалютах'])


@router.get(
    "",
    summary="Получить все криптовалюты",
)
async def get_cryptocurrencies(
    request: Request
):
    """
    Получает все криптовалюты.

    Returns:
        Список всех криптовалют.
    """
    return await request.app.state.cmc_client.get_listings()


@router.get(
    "/{currency_id}",
    summary="Получить криптовалюту по id",
)
async def get_currency(
    currency_id: int,
    request: Request
):
    """
    Получает криптовалюту по ее id.

    Args:
        currency_id (int): id криптовалюты.

    Returns:
        Криптовалюта с указанным id.
    """
    return await request.app.state.cmc_client.get_currency(currency_id)
