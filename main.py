"""
Главный файл программы - точка входа.
"""

from src.api import HHAPI
from src.vacancy import Vacancy
from src.storage import JSONStorage


def main():
    """Главная функция программы."""
    api = HHAPI()
    storage = JSONStorage()

    while True:
        print("\n" + "=" * 50)
        print("ПАРСЕР ВАКАНСИЙ HH.RU")
        print("=" * 50)
        print("1. Поиск и сохранение вакансий")
        print("2. Показать все сохраненные вакансии")
        print("3. Топ-N вакансий по зарплате")
        print("4. Поиск по ключевому слову в описании")
        print("5. Удалить вакансию")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите действие (0-5): ").strip()

        if choice == "1":
            search_vacancies(api, storage)
        elif choice == "2":
            show_all_vacancies(storage)
        elif choice == "3":
            show_top_vacancies(storage)
        elif choice == "4":
            search_by_keyword(storage)
        elif choice == "5":
            delete_vacancy(storage)
        elif choice == "0":
            print("До свидания! 👋")
            break
        else:
            print("Неверный выбор! Пожалуйста, выберите от 0 до 5.")


def search_vacancies(api: HHAPI, storage: JSONStorage):
    """Поиск и сохранение вакансий."""
    keyword = input("Введите ключевое слово для поиска: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым!")
        return

    try:
        count_input = input("Сколько вакансий найти? (10): ").strip()
        count = int(count_input) if count_input else 10

        print("Ищем вакансии...")
        vacancies_data = api.get_vacancies(keyword, count)

        added_count = 0
        for item in vacancies_data:
            # Обрабатываем зарплату
            salary = None
            if item.get("salary"):
                salary_data = item["salary"]
                salary = salary_data.get("from")

            # Создаем объект Vacancy
            vacancy = Vacancy(
                title=item.get("name", "Без названия"),
                url=item.get("alternate_url", ""),
                salary=salary if salary is not None else 0,
                description=item.get("snippet", {}).get("requirement", "")
                or "Нет описания",
            )

            # Сохраняем вакансию
            storage.add_vacancy(vacancy)
            added_count += 1

        print(f"Найдено и сохранено {added_count} вакансий!")

    except Exception as e:
        print(f"Ошибка: {e}")


def show_all_vacancies(storage: JSONStorage):
    """Показать все сохраненные вакансии."""
    vacancies = storage.get_vacancies()

    if not vacancies:
        print("Нет сохраненных вакансий")
        return

    print(f"\nВсе сохраненные вакансии ({len(vacancies)}):")
    print("-" * 50)

    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy}")
        print("-" * 30)


def show_top_vacancies(storage: JSONStorage):
    """Показать топ-N вакансий по зарплате."""
    try:
        n_input = input("Сколько вакансий показать? (5): ").strip()
        n = int(n_input) if n_input else 5

        vacancies = storage.get_vacancies()

        # Создаем список для вакансий с зарплатой больше 0
        vacancies_with_salary = []
        for vacancy in vacancies:
            if vacancy.salary > 0:
                vacancies_with_salary.append(vacancy)

        # Сортируем по зарплате (от большей к меньшей)
        sorted_vacancies = sorted(
            vacancies_with_salary, key=lambda v: v.salary, reverse=True
        )

        # Берем первые N вакансий
        top_vacancies = sorted_vacancies[:n]

        if not top_vacancies:
            print("Нет вакансий с указанной зарплатой")
            return

        print(f"\nТоп-{n} вакансий по зарплате:")
        print("-" * 50)

        for i, vacancy in enumerate(top_vacancies, 1):
            print(f"{i}. {vacancy.title} - {vacancy.salary} руб.")
            print(f"   Ссылка: {vacancy.url}")
            print("-" * 30)

    except ValueError:
        print("Пожалуйста, введите число!")


def search_by_keyword(storage: JSONStorage):
    """Поиск по ключевому слову в описании."""
    keyword = input("Введите ключевое слово для поиска в описании: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым!")
        return

    found_vacancies = storage.filter_by_keyword(keyword)

    if not found_vacancies:
        print(f"Не найдено вакансий с ключевым словом '{keyword}'")
        return

    print(f"\nНайдено {len(found_vacancies)} вакансий с ключевым словом '{keyword}':")
    print("-" * 50)

    for i, vacancy in enumerate(found_vacancies, 1):
        print(f"{i}. {vacancy}")
        print("-" * 30)


def delete_vacancy(storage: JSONStorage):
    """Удаление вакансии по URL."""
    url = input("Введите URL вакансии для удаления: ").strip()
    if not url:
        print("URL не может быть пустым!")
        return

    storage.delete_vacancy(url)
    print("Вакансия удалена (если она существовала)")


if __name__ == "__main__":
    main()
