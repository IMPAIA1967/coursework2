"""
Класс для представления вакансии.
Простая версия без валидации и сложных методов.
"""


class Vacancy:
    """
    Модель вакансии с 4 атрибутами.
    title - название, url - ссылка,
    salary - зарплата, description - описание.
    """

    # Используем __slots__ для экономии памяти
    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: int, description: str):
        """
        Простой конструктор без валидации.
        Просто сохраняем переданные значения.
        """
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description

    def to_dict(self) -> dict:
        """Преобразует вакансию в словарь для сохранения в JSON."""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создает вакансию из словаря."""
        return cls(
            title=data["title"],
            url=data["url"],
            salary=data["salary"],
            description=data["description"]
        )

    def __str__(self) -> str:
        """Красивое строковое представление вакансии."""
        salary_text = f"{self.salary} руб." if self.salary else "Не указана"
        return f"{self.title} - {salary_text}\nСсылка: {self.url}"