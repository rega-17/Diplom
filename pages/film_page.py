# pages/film_page.py
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Tuple


class FilmPage(BasePage):
    """Page Object для страницы фильма."""
    
    # Базовые локаторы (можно оставить пустыми для упрощённого теста)
    REVIEW_INPUT: Tuple[By, str] = (By.CSS_SELECTOR, "textarea, input[name*='review']")
    REVIEW_LENGTH_HINT: Tuple[By, str] = (By.CSS_SELECTOR, ".hint, small, span.info-text")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = None  # URL будет зависеть от фильма
    
    @allure.step("Получить название фильма")
    def get_movie_title(self) -> str:
        """Возвращает название фильма со страницы."""
        try:
            # Попробуем найти заголовок фильма
            title_selectors = [
                (By.CSS_SELECTOR, "h1"),
                (By.CSS_SELECTOR, "[class*='title']"),
                (By.CSS_SELECTOR, "[data-test-id='film-title']")
            ]
            
            for selector in title_selectors:
                try:
                    element = self.find_element(selector, timeout=2)
                    if element:
                        return element.text.strip()
                except:
                    continue
        except:
            pass
        return "Неизвестный фильм"