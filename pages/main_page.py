import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from typing import Tuple


class MainPage(BasePage):
    """Page Object для главной страницы Кинопоиска."""
    
   
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='фильм'], input[placeholder*='поиск'], input[type='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .search-button, [class*='search'] button")
    SEARCH_CLEAR_BUTTON = (By.CSS_SELECTOR, "a[href='/s/']")
    LOGO = (By.CSS_SELECTOR, "a[href='/'], .logo, [class*='logo']")
    MENU = (By.CSS_SELECTOR, "nav, [class*='menu'], [class*='navigation']")
    FOOTER = (By.CSS_SELECTOR, "footer, [class*='footer']")
    
    # Для тестов
    ACTOR_LINKS = (By.CSS_SELECTOR, "a[href*='/name/'], a[href*='/actor/']")
    FILM_LINKS = (By.CSS_SELECTOR, "a[href*='/film/'], a[href*='/movie/']")
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.kinopoisk.ru/"
    
    @allure.step("Открыть главную страницу")
    def open(self):
        """Открывает главную страницу Кинопоиска."""
        self.driver.get(self.url)
        return self
    
    @allure.step("Выполнить поиск по запросу: {query}")
    def search(self, query: str):
        """Выполняет поиск по указанному запросу."""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        return self
    
    @allure.step("Очистить поле поиска")
    def clear_search(self):
        """Очищает поле поиска."""
        # Ждем появления кнопки очистки
        try:
            clear_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.SEARCH_CLEAR_BUTTON)
            )
            clear_btn.click()
        except:
            # Если кнопка не найдена, очищаем через клавиши
            search_field = self.find_element(self.SEARCH_INPUT)
            search_field.send_keys(Keys.CONTROL + "a")
            search_field.send_keys(Keys.DELETE)
        return self
    
    @allure.step("Проверить, что поле поиска пустое")
    def is_search_field_empty(self) -> bool:
        """Проверяет, пустое ли поле поиска."""
        search_field = self.find_element(self.SEARCH_INPUT)
        return search_field.get_attribute("value") == ""
    
    @allure.step("Кликнуть на логотип")
    def click_logo(self):
        """Кликает на логотип для возврата на главную."""
        self.click(self.LOGO)
        return self
    
    @allure.step("Открыть меню")
    def open_menu(self):
        """Открывает главное меню."""
        self.click(self.MENU)
        return self
    
    @allure.step("Получить текст футера")
    def get_footer_text(self) -> str:
        """Возвращает текст футера страницы."""
        footer = self.find_element(self.FOOTER)
        return footer.text.strip()
    
    @allure.step("Получить все ссылки на актёров")
    def get_actor_links(self):
        """Возвращает все ссылки на актёров на странице."""
        return self.find_elements(self.ACTOR_LINKS)
    
    @allure.step("Получить все ссылки на фильмы")
    def get_film_links(self):
        """Возвращает все ссылки на фильмы на странице."""
        return self.find_elements(self.FILM_LINKS)