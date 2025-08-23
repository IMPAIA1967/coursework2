"""
Модуль для работы с API HH.ru
"""
from abc import ABC, abstractmethod
import requests
from typing import List, Dict, Any


class AbstractAPI(ABC):
    """
    Абстрактный класс для работы с API вакансий.
    Это как шаблон, который говорит какие методы должны быть.
    """

    @abstractmethod
    def _connect(self) -> bool:
        """Проверяет, доступно ли API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int) -> List[Dict[str, Any]]:
        """Получает вакансии по ключевому слову."""
        pass


class HHAPI(AbstractAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        # Приватный атрибут (начинается с __)
        self.__base_url = "https://api.hh.ru/vacancies"

    def _connect(self) -> bool:
        """
        Приватный метод проверки подключения к API.
        Отправляет запрос на базовый URL и проверяет статус.
        """
        try:
            response = requests.get(self.__base_url, timeout=5)
            # Если статус 200 - всё хорошо
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_vacancies(self, keyword: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Получает вакансии с HH.ru по ключевому слову.
        Сначала проверяет подключение, потом делает запрос.
        """
        # Вызываем приватный метод проверки подключения
        if not self._connect():
            raise ConnectionError("API HH.ru недоступен")

        # Формируем параметры для запроса
        params = {
            "text": keyword,  # Ключевое слово для поиска
            "per_page": per_page,  # Сколько вакансий получить
            "area": 113  # Код России
        }

        # Отправляем запрос на API HH.ru
        response = requests.get(self.__base_url, params=params)

        # Проверяем, что запрос успешен
        if response.status_code != 200:
            raise Exception(f"Ошибка API: {response.status_code}")

        # Преобразуем ответ в JSON и возвращаем список вакансий
        data = response.json()
        return data.get("items", [])