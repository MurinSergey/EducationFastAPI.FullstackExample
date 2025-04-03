from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from http_client import CMCHttpClient
from config import settings


@asynccontextmanager
async def lifecycle_handler(app: FastAPI):
    """
    Асинхронный контекстный менеджер для обработки жизненного цикла приложения.

    Args:
    app (FastAPI): Приложение FastAPI.

    Yields:
    None
    """
    # Создаем клиент CoinMarketCap HTTP-клиента
    app.state.cmc_client = CMCHttpClient(
        base_url=settings.CMC_BASE_URL,
        api_key=settings.CMC_API_KEY
    )
    yield
    # Закрываем клиент CoinMarketCap HTTP-клиента
    await app.state.cmc_client.close()

app = FastAPI(
    lifespan=lifecycle_handler # Добавляем контекстный менеджер жизненного цикла приложения
)


@app.get(
    "/cryptocurrency",
    summary="Получить все криптовалюты",
)
async def get_cryptocurrencies():
    """
    Получает все криптовалюты.

    Returns:
        Список всех криптовалют.
    """
    return await app.state.cmc_client.get_listings()


@app.get(
    "/cryptocurrency/{currency_id}",
    summary="Получить криптовалюту по id",
)
async def get_currency(currency_id: int):
    """
    Получает криптовалюту по ее id.

    Args:
        currency_id (int): id криптовалюты.

    Returns:
        Криптовалюта с указанным id.
    """
    return await app.state.cmc_client.get_currency(currency_id)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
