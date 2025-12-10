import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.settings import settings


class WebDriverFactory:
    """Фабрика для создания WebDriver."""
    
    @staticmethod
    def create_driver() -> webdriver.Remote:
        """
        Создаёт и возвращает экземпляр WebDriver.
        
        Returns:
            Экземпляр WebDriver
        """
        browser_name = settings.BROWSER.lower()
        headless = settings.HEADLESS
        
        logger = logging.getLogger(__name__)
        logger.info(f"Создание драйвера для {browser_name} (headless: {headless})")
        
        if browser_name == "chrome":
            return WebDriverFactory._create_chrome_driver(headless)
        elif browser_name == "firefox":
            return WebDriverFactory._create_firefox_driver(headless)
        elif browser_name == "edge":
            return WebDriverFactory._create_edge_driver(headless)
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}")
    
    @staticmethod
    def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
        """Создаёт Chrome драйвер."""
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        # Базовые настройки
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        
        # Отключаем логи
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # Используем webdriver_manager для автоматической загрузки драйвера
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    @staticmethod
    def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Создаёт Firefox драйвер."""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        service = webdriver.firefox.service.Service(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    @staticmethod
    def _create_edge_driver(headless: bool) -> webdriver.Edge:
        """Создаёт Edge драйвер."""
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        service = webdriver.edge.service.Service(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    
def create_driver() -> webdriver.Remote:
    """
    Упрощённая функция для создания драйвера.
    
    Returns:
        Экземпляр WebDriver
    """
    return WebDriverFactory.create_driver()