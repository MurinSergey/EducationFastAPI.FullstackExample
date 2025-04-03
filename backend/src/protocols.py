from typing import Protocol


class http_client(Protocol):
    """
    Класс http_client, который является протоколом для работы с HTTP-запросами.
    """
    def get_all(self) -> dict:
        """
        Метод get_all возвращает все данные в виде словаря.
        """
        ...

    def get_by_id(self, id: int) -> dict:
        """
        Метод get_by_id возвращает данные по заданному идентификатору в виде словаря.
        :param id: Идентификатор данных, которые нужно получить.
        """
        ...