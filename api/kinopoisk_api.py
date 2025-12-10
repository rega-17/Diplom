import allure
from typing import Dict, Any, Optional, List
from api.base_api import BaseAPI
from config.settings import settings


class KinopoiskAPI(BaseAPI):
    """Класс для работы с API Кинопоиска."""
    
    def __init__(self):
        """Инициализация API клиента для Кинопоиска."""
        super().__init__(
            base_url=settings.API_URL,
            headers=settings.api_headers
        )
    
    @allure.step("Поиск фильма")
    def search_movie(self, query: str, page: int = 1, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """Ищет фильмы по названию."""
        params = {
            "page": page,
            "limit": limit,
            "query": query,
            **kwargs
        }
        
        response = self.get("movie/search", params=params)
        self.assert_status_code(response, 200)
        
        return self.assert_json_contains(response, "docs")
    
    @allure.step("Упрощённый поиск фильма")
    def search_movie_simple(self, query: str) -> List[Dict[str, Any]]:
        """Ищет фильмы по названию и возвращает список результатов."""
        result = self.search_movie(query, limit=5)
        return result.get("docs", [])
    
    @allure.step("Получение информации о фильме")
    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any]:
        """Получает информацию о фильме по его ID."""
        response = self.get(f"movie/{movie_id}")
        self.assert_status_code(response, 200)
        return response.json()
    
    @allure.step("Проверка найденного фильма")
    def assert_movie_found(self, query: str, expected_min_results: int = 1) -> List[Dict[str, Any]]:
        """Проверяет что поиск фильма возвращает результаты."""
        movies = self.search_movie_simple(query)
        
        assert len(movies) >= expected_min_results, \
            f"По запросу '{query}' найдено {len(movies)} результатов, " \
            f"ожидалось минимум {expected_min_results}"
        
        allure.attach(
            f"Найдено фильмов: {len(movies)}\nПервый фильм: {movies[0].get('name', 'Нет названия')} ({movies[0].get('year', 'Нет года')})",
            name="Результаты поиска",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return movies
    
    @allure.step("Проверка ненайденного фильма")
    def assert_movie_not_found(self, query: str) -> None:
        """Проверяет что поиск фильма НЕ возвращает результатов."""
        movies = self.search_movie_simple(query)
        
        assert len(movies) == 0, \
            f"По запросу '{query}' неожиданно найдено {len(movies)} результатов"
        
        allure.attach(
            f"По запросу '{query}' правильно не найдено результатов",
            name="Результаты негативного поиска",
            attachment_type=allure.attachment_type.TEXT
        )
