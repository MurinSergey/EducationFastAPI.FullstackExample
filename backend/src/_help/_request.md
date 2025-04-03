### **Что такое `Request` в FastAPI?**  
`Request` — это объект, который содержит всю информацию о входящем HTTP-запросе:  
- Заголовки (`headers`)  
- Параметры URL (`path`, `query`)  
- Тело запроса (`body`)  
- Куки (`cookies`)  
- Данные формы (`form data`)  
- Состояние приложения (`app.state`)  

FastAPI автоматически создает этот объект для каждого запроса и передает его в зависимости или эндпоинты, если они его запрашивают.

---

### **Зачем передавать `Request` в эндпоинт?**  
1. **Доступ к `app.state`**  
   В вашем случае `app.state.cmc_client` хранит клиент API (например, для CoinMarketCap). Через `Request` можно получить доступ к этому клиенту:
   ```python
   @router.get("/price")
   async def get_price(request: Request):
       client = request.app.state.cmc_client  # Получаем клиента
       price = await client.get_price("BTC")
       return {"price": price}
   ```

2. **Чтение метаданных запроса**  
   Например, можно получить IP пользователя или заголовки:
   ```python
   @router.get("/info")
   async def get_info(request: Request):
       client_ip = request.client.host  # IP-адрес клиента
       user_agent = request.headers["User-Agent"]  # Браузер пользователя
       return {"ip": client_ip, "user_agent": user_agent}
   ```

3. **Работа с куками и сессиями**  
   ```python
   @router.get("/login")
   async def login(request: Request):
       request.session["user"] = "admin"  # Установка куки
   ```

---

### **Как это работает?**  
1. **FastAPI создает `Request`**  
   При каждом HTTP-запросе FastAPI автоматически генерирует объект `Request`.

2. **Передает его в эндпоинт**  
   Если эндпоинт объявляет параметр `request: Request`, FastAPI подставит туда этот объект.

3. **Доступ к данным**  
   Вы можете извлекать данные запроса или (как в вашем случае) получать доступ к глобальным объектам приложения (`app.state`).

---

### **Альтернатива: Dependency Injection (лучший способ)**  
Вместо явного использования `Request` можно создать **зависимость**, которая будет возвращать клиента:  
```python
# dependencies.py
from fastapi import Request, Depends

def get_cmc_client(request: Request):
    return request.app.state.cmc_client

# В роутере
@router.get("/price/{symbol}")
async def get_price(
    symbol: str,
    client: CMCHttpClient = Depends(get_cmc_client)  # FastAPI автоматически внедрит клиента
):
    price = await client.get_price(symbol)
    return {"price": price}
```
**Плюсы:**  
- Чище код (не нужно вручную работать с `Request`).  
- Легче тестировать (можно подменить `get_cmc_client` в тестах).  

---

### **Вывод**  
- **`Request`** — это "входная точка" для работы с запросом и состоянием приложения.  
- **Если нужно только `app.state.cmc_client`** → используйте **Dependency Injection** (через `Depends`), это удобнее.  
- **Если нужны заголовки, куки или IP** → используйте `Request` напрямую.  

Пример с `Depends` (**рекомендуемый способ**):
```python
from fastapi import APIRouter, Depends
from .dependencies import get_cmc_client

router = APIRouter()

@router.get("/price/{symbol}")
async def get_price(
    symbol: str,
    client: CMCHttpClient = Depends(get_cmc_client)
):
    return await client.get_price(symbol)
```