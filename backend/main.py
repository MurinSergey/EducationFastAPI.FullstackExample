from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from src.dependencies import setup_cmc_client
from src.cryptocurrency.router import router as cmc_router


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
    app.state.cmc_client = setup_cmc_client()
    yield
    # Закрываем клиент CoinMarketCap HTTP-клиента
    await app.state.cmc_client.close()

def get_app() -> FastAPI:
    """
    Создает и возвращает экземпляр приложения FastAPI.

    Returns:
    FastAPI: Экземпляр приложения FastAPI.
    """
    app = FastAPI(
        # Добавляем контекстный менеджер жизненного цикла приложения
        lifespan=lifecycle_handler
    )
    # Добавляем роутер криптовалют
    app.include_router(router=cmc_router)
    return app

# Получаем экземпляр приложения FastAPI
app = get_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
