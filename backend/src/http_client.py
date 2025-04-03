from aiohttp import ClientSession


class HttpClient():
    """
    Класс HttpClient используется для создания HTTP-сессии с заданным базовым URL и API-ключом.

    Атрибуты
    ----------
    _session : ClientSession
        HTTP-сессия, созданная с использованием заданного базового URL и API-ключа.

    Методы
    -------
    __init__(base_url: str, api_key: str)
        Конструктор класса HttpClient. Создает HTTP-сессию с заданным базовым URL и API-ключом.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Конструктор класса HttpClient.

        Параметры
        ----------
        base_url : str
        Базовый URL для HTTP-сессии.
        api_key : str
        API-ключ для HTTP-сессии.
        """
        self._session = ClientSession(
            base_url=base_url,
            headers={
                "X-CMC_PRO_API_KEY": api_key,
            }
        )

    async def close(self):
        """
        Метод close закрывает HTTP-сессию.
        """
        await self._session.close()


class CMCHttpClient(HttpClient):
    """
    Класс CMCHttpClient наследует от HttpClient и предоставляет методы для работы с API CoinMarketCap.
    """

    async def get_listings(self):
        """
        Метод get_listings делает асинхронный GET запрос к API CoinMarketCap для получения списка криптовалют.
        Возвращает список криптовалют в формате JSON.

        Returns:
            dict: Словарь c данными о криптовалютах.
        """
        async with self._session.get('/v1/cryptocurrency/listings/latest') as response:
            result = await response.json()
            return result["data"]

    async def get_currency(self, currency_id: int):
        """
        Метод get_currency_info делает асинхронный GET запрос к API CoinMarketCap для получения информации о криптовалюте по ее ID.
        Возвращает информацию о криптовалюте в формате JSON.

        Args:
            currency_id (int): ID криптовалюты.

        Returns:
            dict: Словарь с данными о криптовалюте.
        """
        async with self._session.get(
            url='/v2/cryptocurrency/quotes/latest',
            params={'id': currency_id}
        ) as response:
            result = await response.json()
            return result["data"][str(currency_id)]