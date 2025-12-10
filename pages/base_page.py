"""
Базовый класс для всех страниц.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import settings


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver: WebDriver, timeout: int = None):
        """
        Инициализация базовой страницы.

        Args:
            driver: Экземпляр WebDriver
            timeout: Таймаут для явных ожиданий (секунды)
        """
        self.driver = driver
        # ИСПРАВЛЕНО: используем settings.wait_timeout вместо settings.EXPLICIT_WAIT
        self.timeout = timeout or settings.wait_timeout
        self.wait = WebDriverWait(driver, self.timeout)
        self.base_url = settings.base_url

    def open(self, url: str = "") -> None:
        """
        Открывает указанный URL.

        Args:
            url: Относительный URL (будет добавлен к base_url)
        """
        full_url = f"{self.base_url}{url}"
        self.driver.get(full_url)

    def find_element(self, locator: tuple, timeout: int = None):
        """
        Находит элемент с ожиданием.

        Args:
            locator: Локатор элемента (кортеж)
            timeout: Время ожидания

        Returns:
            WebElement: Найденный элемент
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_clickable_element(self, locator: tuple, timeout: int = None):
        """
        Находит кликабельный элемент с ожиданием.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания

        Returns:
            WebElement: Найденный элемент
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def find_visible_element(self, locator: tuple, timeout: int = None):
        """
        Находит видимый элемент с ожиданием.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания

        Returns:
            WebElement: Найденный элемент
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def is_element_present(self, locator: tuple, timeout: int = None) -> bool:
        """
        Проверяет наличие элемента на странице.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания

        Returns:
            bool: True если элемент присутствует
        """
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Проверяет видимость элемента на странице.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания

        Returns:
            bool: True если элемент видим
        """
        try:
            self.find_visible_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator: tuple, timeout: int = None) -> bool:
        """
        Проверяет кликабельность элемента.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания

        Returns:
            bool: True если элемент кликабелен
        """
        try:
            self.find_clickable_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, text: str, timeout: int = None) -> bool:
        """
        Ожидает появления текста в URL.

        Args:
            text: Текст для поиска в URL
            timeout: Время ожидания

        Returns:
            bool: True если текст появился в URL
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.url_contains(text))

    def get_current_url(self) -> str:
        """
        Возвращает текущий URL.

        Returns:
            str: Текущий URL
        """
        return self.driver.current_url

    def refresh(self) -> None:
        """Обновляет текущую страницу."""
        self.driver.refresh()

    def go_back(self) -> None:
        """Возвращается на предыдущую страницу."""
        self.driver.back()

    def go_forward(self) -> None:
        """Переходит на следующую страницу."""
        self.driver.forward()

    def get_title(self) -> str:
        """
        Возвращает заголовок страницы.

        Returns:
            str: Заголовок страницы
        """
        return self.driver.title