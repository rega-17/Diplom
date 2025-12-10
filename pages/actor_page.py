import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Tuple


class ActorPage(BasePage):
    """Page Object для страницы актёра."""
    
    # Локаторы
    ACTOR_NAME: Tuple[By, str] = (By.CSS_SELECTOR, "h1.actor_name")
    ACTOR_BIO: Tuple[By, str] = (By.CSS_SELECTOR, "div.biography")
    FILMOGRAPHY: Tuple[By, str] = (By.CSS_SELECTOR, "section.filmography")
    FILM_LINKS: Tuple[By, str] = (By.CSS_SELECTOR, "a.film_link")
    
    # Навигация
    BACK_BUTTON: Tuple[By, str] = (By.CSS_SELECTOR, "a.back, button.back")
    
    def __init__(self, driver):
        """Инициализация страницы актёра."""
        super().__init__(driver)
    
    @allure.step("Получение имени актёра")
    def get_actor_name(self) -> str:
        """Возвращает имя актёра."""
        return self.get_text(self.ACTOR_NAME)
    
    @allure.step("Проверка что страница актёра загружена")
    def assert_actor_page_loaded(self, expected_name: str = None) -> None:
        """
        Проверяет что страница актёра загружена.
        
        Args:
            expected_name: Ожидаемое имя актёра (если указано)
        """
        self.assert_element_visible(self.ACTOR_NAME)
        self.assert_element_visible(self.ACTOR_BIO)
        
        if expected_name:
            actual_name = self.get_actor_name()
            assert expected_name in actual_name, \
                f"Имя актёра не совпадает. Ожидалось: '{expected_name}', получено: '{actual_name}'"
        
        allure.attach(
            f"Страница актёра загружена: {self.get_actor_name()}",
            name="Загрузка страницы актёра",
            attachment_type=allure.attachment_type.TEXT
        )