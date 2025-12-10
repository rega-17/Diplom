import pytest
import allure
import sys
from selenium import webdriver
from typing import Generator
from pages.main_page import MainPage
from pages.film_page import FilmPage
from pages.actor_page import ActorPage

# Пробуем импортировать simple_driver, если не получится - обычный
try:
    from utils.simple_driver import create_simple_driver
    create_driver = create_simple_driver
    print("✅ Используем simple_driver")
except ImportError as e:
    from utils.driver import create_driver
    print(f"⚠️ Используем обычный driver (simple_driver не найден: {e})")

@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    """
    Фикстура для создания WebDriver.
    Scope: function (новый драйвер для каждого теста)
    """
    driver = None
    try:
        driver = create_driver()
        driver.implicitly_wait(10)
        driver.maximize_window()
        
        yield driver
        
    finally:
        if driver:
            driver.quit()


@pytest.fixture
def main_page(driver: webdriver.Remote) -> MainPage:
    """Фикстура для главной страницы."""
    return MainPage(driver)


@pytest.fixture
def film_page(driver: webdriver.Remote) -> FilmPage:
    """Фикстура для страницы фильма."""
    return FilmPage(driver)


@pytest.fixture
def actor_page(driver: webdriver.Remote) -> ActorPage:
    """Фикстура для страницы актёра."""
    return ActorPage(driver)


def pytest_configure(config):
    """Конфигурация pytest."""
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )


def pytest_collection_modifyitems(config, items):
    """Модификация собранных тестов."""
    for item in items:
        # Автоматически помечаем тесты из test_ui.py как UI тесты
        if "test_ui.py" in item.nodeid:
            item.add_marker(pytest.mark.ui)
        # Автоматически помечаем тесты из test_api.py как API тесты  
        elif "test_api.py" in item.nodeid:
            item.add_marker(pytest.mark.api)