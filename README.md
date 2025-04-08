# Ученый проект
Проект создан по туториалу:
https://vkvideo.ru/video-227148184_456239030
https://github.com/artemonsh/fullstack-fastapi-react

## Мои модификации:
* В классе клиента HTTP добавил метод для закрытия сессии, который вызывается при закрытии приложения FastAPI
* Перенес создание клиента HTTP в асинхронный контекстный менеджер, теперь жизнь клиента HTTP зависит от жизни приложения FastAPI и выполняется в его async event loop
* Использовал внедрение зависимостей для подключения Request в ручки APIRouter через Protocol

## Стек
- FastAPI + pydantic, pydantic-settings, aiohttp
- React + axios, ant design, tailwind

#### Frontend
- `npm create vite@latest`
- `npm install`
- `npm run dev`
