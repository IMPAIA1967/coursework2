"""
Модуль для работы с JSON-файлом.
"""

from abc import ABC, abstractmethod
import json
import os
from typing import List
from .vacancy import Vacancy


class AbstractStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем.
    Определяет какие методы должны быть у любого хранилища.
    """

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        """Получает все вакансии из хранилища."""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище."""
        pass

    @abstractmethod
    def delete_vacancy(self, url: str) -> None:
        """Удаляет вакансию из хранилища."""
        pass

    @abstractmethod
    def filter_by_keyword(self, keyword: str) -> List[Vacancy]:
        """Ищет вакансии по ключевому слову."""
        pass


class JSONStorage(AbstractStorage):
    """Класс для работы с JSON-файлом."""

    def __init__(self, filename: str = "data/vacancies.json"):
        # Приватный атрибут с именем файла
        self.__filename = filename
        # Создаем папку если её нет
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Создаем файл если его нет
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def get_vacancies(self) -> List[Vacancy]:
        """Читает все вакансии из файла."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Создаем список для результатов
            vacancies = []
            # Проходим по всем элементам из файла
            for item in data:
                # Создаем объект Vacancy из словаря
                vacancy = Vacancy.from_dict(item)
                # Добавляем в список результатов
                vacancies.append(vacancy)

            return vacancies

        except (json.JSONDecodeError, FileNotFoundError):
            # Если файл пустой или его нет, возвращаем пустой список
            return []

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию, проверяя чтобы не было дубликатов."""
        # Получаем все текущие вакансии
        vacancies = self.get_vacancies()

        # Проверяем, нет ли уже вакансии с таким URL
        already_exists = False
        for existing_vacancy in vacancies:
            if existing_vacancy.url == vacancy.url:
                already_exists = True
                break

        # Если такой вакансии еще нет, добавляем её
        if not already_exists:
            vacancies.append(vacancy)
            self.__save_vacancies(vacancies)

    def delete_vacancy(self, url: str) -> None:
        """Удаляет вакансию по URL."""
        vacancies = self.get_vacancies()

        # Создаем новый список без вакансии с указанным URL
        new_vacancies = []
        for vacancy in vacancies:
            if vacancy.url != url:
                new_vacancies.append(vacancy)

        # Сохраняем новый список
        self.__save_vacancies(new_vacancies)

    def filter_by_keyword(self, keyword: str) -> List[Vacancy]:
        """Ищет вакансии по ключевому слову в описании."""
        vacancies = self.get_vacancies()
        keyword = keyword.lower()

        # Создаем список для результатов поиска
        found_vacancies = []

        # Проходим по всем вакансиям
        for vacancy in vacancies:
            # Ищем ключевое слово в описании (приводим к нижнему регистру)
            if keyword in vacancy.description.lower():
                found_vacancies.append(vacancy)

        return found_vacancies

    def __save_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Приватный метод для сохранения вакансий в файл."""
        # Преобразуем вакансии в словари
        data = []
        for vacancy in vacancies:
            data.append(vacancy.to_dict())

        # Записываем в файл
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
