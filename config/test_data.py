from typing import Dict, Any, List


class TestData:
    """Класс для хранения тестовых данных."""
    
    # Данные для API тестов (поиск фильмов)
    FILM_NAMES: Dict[str, str] = {
        "russian": "Зеленая миля",
        "latin": "The Green Mile", 
        "numeric": "1999",
        "non_existent": "ываываываываываываыва",
        "future_film": "Фильм 2050 года"
    }
    
    # Данные для UI тестов (поиск)
    SEARCH_QUERIES: Dict[str, str] = {
        "film": "Интерстеллар",
        "actor": "Мэттью Макконахи",
        "series": "Игра престолов",
        "clear_search": "Текст для очистки"
    }
    
    # Ожидаемые результаты
    EXPECTED_YEARS: Dict[str, int] = {
        "Зеленая миля": 1999,
        "Интерстеллар": 2014,
        "The Green Mile": 1999
    }
    
    # Текст для проверки отзыва
    REVIEW_TEXT: str = "Это тестовый отзыв " * 50  # ~1000 символов
    REVIEW_TEXT_TOO_LONG: str = "Слишком длинный отзыв " * 100  # >1000 символов
    
    # URL пути
    URL_PATHS: Dict[str, str] = {
        "main": "/",
        "film": "/film/",
        "actor": "/name/"
    }
    

# Создаём экземпляр с тестовыми данными
test_data = TestData()
SEARCH_QUERIES = [
    test_data.FILM_NAMES["russian"],
    test_data.FILM_NAMES["latin"],
    "Матрица",
    "Интерстеллар",
    "Побег из Шоушенка",
]

EXPECTED_RESULTS = [
    "id",
    "name",
    "year",
    "description",
    "rating",
    "poster",
]

# Экспортируем все необходимое
__all__ = ['test_data', 'TestData', 'SEARCH_QUERIES', 'EXPECTED_RESULTS']
# Данные для API тестов (словарь для совместимости с test_api.py)
SEARCH_QUERIES = {
    "cyrillic": test_data.FILM_NAMES["russian"],  # "Зеленая миля"
    "numbers": "1999",  # год как строка из цифр
    "latin": test_data.FILM_NAMES["latin"],  # "The Green Mile"
    "nonexistent": test_data.FILM_NAMES["non_existent"],  # "ываываываываываываыва"
    "future": test_data.FILM_NAMES["future_film"],  # "Фильм 2050 года"
}

# Ожидаемые поля в ответе
EXPECTED_RESULTS = [
    "id",
    "name", 
    "year",
    "description",
    "rating",
    "poster",
]

__all__ = ['test_data', 'TestData', 'SEARCH_QUERIES', 'EXPECTED_RESULTS']