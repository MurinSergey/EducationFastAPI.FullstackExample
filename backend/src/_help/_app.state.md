Если вы используете **роутеры (APIRouter)** в FastAPI, то передача клиента в эндпоинты будет немного отличаться. Вот как правильно организовать работу с клиентом в роутерах:

---

## 🔧 **Способ 1: Через Request (простой способ)**

### 1. В основном файле (`main.py`):
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import crypto_router  # импортируем роутер

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация клиента
    from src.http_client import CMCHttpClient
    from src.config import settings
    app.state.cmc_client = CMCHttpClient(
        base_url=settings.CMC_BASE_URL,
        api_key=settings.CMC_API_KEY
    )
    yield
    # Закрытие клиента
    await app.state.cmc_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(crypto_router)  # подключаем роутер
```

### 2. В роутере (`routers/crypto.py`):
```python
from fastapi import APIRouter, Request, Depends
from src.http_client import CMCHttpClient

router = APIRouter(prefix="/api/crypto")

# Способ 1: Через Request
@router.get("/price/{symbol}")
async def get_price(symbol: str, request: Request):
    client = request.app.state.cmc_client
    price = await client.get_price(symbol)
    return {"symbol": symbol, "price": price}
```

---

## 🛠 **Способ 2: Через зависимости (более чистый вариант)**

### 1. Создаём файл `dependencies.py`:
```python
from fastapi import Request, Depends
from src.http_client import CMCHttpClient

async def get_cmc_client(request: Request) -> CMCHttpClient:
    return request.app.state.cmc_client
```

### 2. Используем в роутере:
```python
from fastapi import APIRouter, Depends
from .dependencies import get_cmc_client
from src.http_client import CMCHttpClient

router = APIRouter(prefix="/api/crypto")

# Способ 2: Через Depends
@router.get("/price/{symbol}")
async def get_price(
    symbol: str,
    client: CMCHttpClient = Depends(get_cmc_client)
):
    price = await client.get_price(symbol)
    return {"symbol": symbol, "price": price}
```

---

## 🔄 **Способ 3: Через роутер с зависимостями (если нужно передать клиент в несколько роутеров)**

### 1. Создаём роутер с зависимостями:
```python
from fastapi import APIRouter, Depends
from src.http_client import CMCHttpClient

def create_crypto_router(client: CMCHttpClient) -> APIRouter:
    router = APIRouter(prefix="/api/crypto")

    @router.get("/price/{symbol}")
    async def get_price(symbol: str):
        price = await client.get_price(symbol)
        return {"symbol": symbol, "price": price}
    
    return router
```

### 2. В `main.py`:
```python
# После инициализации клиента:
from .routers.crypto import create_crypto_router
crypto_router = create_crypto_router(app.state.cmc_client)
app.include_router(crypto_router)
```

---

## ⚠ **Важные моменты:**
1. **Не создавайте новый клиент в каждом запросе** – используйте существующий из `app.state`.
2. **Все методы клиента должны быть `async`**, так как работаете с `aiohttp`.
3. **Для тестирования** можно подменить `app.state.cmc_client` на mock-объект.

---

## 🏆 **Лучшая практика:**
Для больших проектов лучше использовать **Способ 2** (зависимости), так как:
- Чистая инъекция зависимостей
- Легко тестировать
- Понятная структура кода

Пример полной реализации:
```python
# routers/crypto.py
from fastapi import APIRouter, Depends
from src.http_client import CMCHttpClient

router = APIRouter(prefix="/crypto")

@router.get("/price/{symbol}")
async def get_crypto_price(
    symbol: str,
    client: CMCHttpClient = Depends(get_cmc_client)
):
    return await client.get_price(symbol)
```