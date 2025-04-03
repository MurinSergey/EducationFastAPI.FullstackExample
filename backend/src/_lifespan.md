### **`@asynccontextmanager` и `lifespan` в FastAPI**  

Эти инструменты нужны для управления **жизненным циклом приложения** — они позволяют выполнять код при старте сервера (инициализация ресурсов) и при его остановке (очистка).  

---

## **1. Что делает `@asynccontextmanager`?**  
Это **декоратор** из модуля `contextlib`, который превращает асинхронную функцию в **контекстный менеджер**.  

### Пример без FastAPI:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def db_connection():
    print("Подключаемся к БД")  # Код при входе
    yield "connection"          # Объект, который будет доступен внутри блока
    print("Отключаемся от БД")  # Код при выходе

# Использование:
async def main():
    async with db_connection() as conn:
        print(f"Используем соединение: {conn}")
```
**Вывод:**
```
Подключаемся к БД
Используем соединение: connection
Отключаемся от БД
```

---

## **2. Как это работает в FastAPI (`lifespan`)?**  
FastAPI использует `lifespan` для управления ресурсами (БД, кеш, HTTP-клиенты и т.д.).  

### Пример с FastAPI:
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код выполняется ПРИ СТАРТЕ сервера
    print("Сервер запускается")
    app.state.db = "Подключение к БД установлено"
    
    yield  # Здесь FastAPI работает в обычном режиме
    
    # Код выполняется ПРИ ОСТАНОВКЕ сервера
    print("Сервер останавливается")
    app.state.db = None  # Закрываем соединение

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"db_status": app.state.db}
```

### **Что происходит:**
1. При старте сервера:
   - Выполняется код до `yield` (инициализация ресурсов).
   - `app.state` заполняется данными (например, подключение к БД).
2. Во время работы сервера:
   - FastAPI обрабатывает запросы.
   - Можно использовать `app.state` в эндпоинтах.
3. При остановке сервера (Ctrl+C):
   - Выполняется код после `yield` (очистка ресурсов).

---

## **3. Зачем это нужно?**  
### **Проблемы без `lifespan`:**
- Если инициализировать ресурсы (клиенты API, БД) **на уровне модуля**, они могут создаться **до запуска event loop** → ошибки.
- Если не закрывать соединения при остановке сервера → утечки ресурсов.

### **Решение с `lifespan`:**
- **Инициализация при старте**:  
  Создание клиентов, подключение к БД, загрузка моделей ML.
- **Очистка при остановке**:  
  Корректное закрытие соединений, сохранение состояния.

---

## **4. Реальный пример: HTTP-клиент + БД**
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiohttp import ClientSession
from databases import Database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация клиента и БД
    app.state.http_client = ClientSession()
    app.state.db = Database("sqlite:///db.sqlite")
    await app.state.db.connect()
    
    yield
    
    # Очистка
    await app.state.http_client.close()
    await app.state.db.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/data")
async def get_data():
    # Используем клиент и БД из app.state
    async with app.state.http_client.get("https://api.example.com/data") as resp:
        data = await resp.json()
    
    db_data = await app.state.db.fetch_all("SELECT * FROM items")
    return {"api_data": data, "db_data": db_data}
```

---

## **5. Альтернативы (для старых версий FastAPI)**
Раньше использовались `startup` и `shutdown` события:
```python
app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.http_client = ClientSession()

@app.on_event("shutdown")
async def shutdown():
    await app.state.http_client.close()
```
**Но `lifespan` лучше**, потому что:
- Более явное управление ресурсами.
- Легче тестировать.
- Поддержка async/await.

---

## **Вывод**  
- **`@asynccontextmanager`** — превращает асинхронную функцию в контекстный менеджер.  
- **`lifespan`** в FastAPI — замена `startup/shutdown`, которая гарантирует:  
  - Инициализацию ресурсов **после** запуска event loop.  
  - Корректную очистку при остановке сервера.  
- Используйте для: HTTP-клиентов, подключений к БД, кешей и других долгоживущих объектов.  

**Итоговый шаблон:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация
    app.state.client = MyClient()
    yield
    # Очистка
    await app.state.client.close()

app = FastAPI(lifespan=lifespan)
```