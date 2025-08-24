import os
import tempfile
from src.api import HHAPI
from src.vacancy import Vacancy
from src.storage import JSONStorage


def test_vacancy_creation():
    """Проверяем, что вакансия создаётся и превращается в словарь."""
    v = Vacancy("Python dev", "http://test.com", 100000, "Опыт 1 год")
    assert v.title == "Python dev"
    assert v.salary == 100000
    assert v.to_dict()["url"] == "http://test.com"


def test_storage_add_and_get():
    """Проверяем добавление и чтение одной вакансии."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    storage = JSONStorage(tmp_path)
    vac = Vacancy("QA", "http://qa.ru", 80000, "Тесты")
    storage.add_vacancy(vac)

    loaded = storage.get_vacancies()
    assert len(loaded) == 1
    assert loaded[0].title == "QA"

    os.remove(tmp_path)  # убираем временный файл


def test_storage_no_duplicates():
    """Одинаковые URL не должны дублироваться."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    storage = JSONStorage(tmp_path)
    v1 = Vacancy("A", "http://same", 1, "desc")
    v2 = Vacancy("B", "http://same", 2, "desc")
    storage.add_vacancy(v1)
    storage.add_vacancy(v2)

    assert len(storage.get_vacancies()) == 1

    os.remove(tmp_path)


def test_storage_delete():
    """Проверяем удаление по URL."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    storage = JSONStorage(tmp_path)
    vac = Vacancy("Del", "http://del.ru", 200, "del")
    storage.add_vacancy(vac)
    storage.delete_vacancy("http://del.ru")

    assert len(storage.get_vacancies()) == 0

    os.remove(tmp_path)


# ---------- 3. Тесты HHAPI ----------
def test_api_connect():
    """API должен быть доступен (код 200)."""
    api = HHAPI()
    assert api._connect() is True


def test_api_get_vacancies():
    """Получаем хотя бы одну вакансию по слову 'python'."""
    api = HHAPI()
    items = api.get_vacancies("python", per_page=1)
    assert isinstance(items, list)
    assert len(items) == 1
    assert "name" in items[0]  # у вакансии есть название
