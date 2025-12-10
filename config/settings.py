"""
Настройки и конфигурация для тестов Кинопоиска.
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

# Определение базовой директории проекта
BASE_DIR = Path(__file__).parent.parent

# Загружаем .env файл вручную
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if (
                    (value.startswith('"') and value.endswith('"'))
                    or (value.startswith("'") and value.endswith("'"))
                ):
                    value = value[1:-1]
                os.environ[key] = value


@dataclass
class Settings:
    """Класс для хранения всех настроек тестов."""

    # API настройки
    api_url: str = "https://api.kinopoisk.dev/v1.4"
    api_key: Optional[str] = None
    api_timeout: int = 30
    api_connect_timeout: int = 10
    api_read_timeout: int = 30
    api_max_retries: int = 3
    api_retry_delay: int = 2

    # UI настройки
    base_url: str = "https://www.kinopoisk.ru"
    browser: str = "chrome"
    headless: bool = False
    window_width: int = 1920
    window_height: int = 1080

    # Таймауты WebDriver
    driver_timeout: int = 30
    driver_implicit_wait: int = 5
    driver_page_load_timeout: int = 60

    # Настройки ожиданий
    wait_timeout: int = 20
    poll_frequency: float = 0.5

    # Настройки тестов
    captcha_wait_time: int = 20
    action_delay: float = 0.5
    short_delay: float = 1.0
    long_delay: float = 3.0

    # Настройки логирования
    log_level: str = "INFO"

    # Пути к директориям
    screenshots_dir: Path = BASE_DIR / "screenshots"
    logs_dir: Path = BASE_DIR / "logs"
    test_data_dir: Path = BASE_DIR / "test_data"
    allure_results_dir: Path = BASE_DIR / "allure-results"

    def __init__(self):
        """Инициализация настроек из переменных окружения."""
        # Загрузка API настроек
        self.api_url = os.getenv("API_URL", self.api_url)
        self.api_key = os.getenv("API_KEY") or os.getenv("KINOPOISK_API_KEY")

        # Загрузка числовых параметров API
        self._load_int_env("API_TIMEOUT", "api_timeout")
        self._load_int_env("API_CONNECT_TIMEOUT", "api_connect_timeout")
        self._load_int_env("API_READ_TIMEOUT", "api_read_timeout")
        self._load_int_env("API_MAX_RETRIES", "api_max_retries")
        self._load_int_env("API_RETRY_DELAY", "api_retry_delay")

        # Загрузка UI настроек
        self.base_url = os.getenv("BASE_URL", self.base_url)
        self.browser = os.getenv("BROWSER", self.browser)

        # Загрузка булевых значений
        headless_env = os.getenv("HEADLESS", "").lower()
        self.headless = headless_env in ("true", "1", "yes", "y")

        # Загрузка размеров окна
        self._load_int_env("WINDOW_WIDTH", "window_width")
        self._load_int_env("WINDOW_HEIGHT", "window_height")

        # Загрузка таймаутов WebDriver
        self._load_int_env("DRIVER_TIMEOUT", "driver_timeout")
        self._load_int_env("DRIVER_IMPLICIT_WAIT", "driver_implicit_wait")
        self._load_int_env("DRIVER_PAGE_LOAD_TIMEOUT", "driver_page_load_timeout")

        # Загрузка настроек ожиданий
        self._load_int_env("WAIT_TIMEOUT", "wait_timeout")
        self._load_float_env("POLL_FREQUENCY", "poll_frequency")

        # Загрузка настроек тестов
        self._load_int_env("CAPTCHA_WAIT_TIME", "captcha_wait_time")
        self._load_float_env("ACTION_DELAY", "action_delay")
        self._load_float_env("SHORT_DELAY", "short_delay")
        self._load_float_env("LONG_DELAY", "long_delay")

        # Загрузка настроек логирования
        self.log_level = os.getenv("LOG_LEVEL", self.log_level).upper()

        # Создание директорий
        self._create_directories()

    def _load_int_env(self, env_name: str, attr_name: str) -> None:
        """Загрузить целочисленную переменную окружения."""
        env_value = os.getenv(env_name)
        if env_value and env_value.isdigit():
            setattr(self, attr_name, int(env_value))

    def _load_float_env(self, env_name: str, attr_name: str) -> None:
        """Загрузить переменную окружения с плавающей точкой."""
        env_value = os.getenv(env_name)
        if env_value:
            try:
                setattr(self, attr_name, float(env_value))
            except ValueError:
                pass

    def _create_directories(self) -> None:
        """Создать необходимые директории для работы тестов."""
        directories = [
            self.screenshots_dir,
            self.logs_dir,
            self.test_data_dir,
            self.allure_results_dir,
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True, parents=True)

    @property
    def is_api_configured(self) -> bool:
        """Проверить, настроен ли API ключ."""
        return bool(self.api_key)

    @property
    def api_headers(self) -> dict:
        """Получить заголовки для API запросов."""
        if not self.api_key:
            return {}

        return {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def print_config_summary(self) -> None:
        """Вывести сводку конфигурации."""
        print("=" * 60)
        print("КОНФИГУРАЦИЯ ТЕСТОВ КИНОПОИСК")
        print("=" * 60)
        print()

        # API настройки
        print("📡 API Настройки:")
        print(f"  URL: {self.api_url}")
        print(f"  Ключ: {'УСТАНОВЛЕН' if self.api_key else 'НЕ УСТАНОВЛЕН'}")
        if self.api_key:
            print(f"  Ключ (маскированный): ****{self.api_key[-4:]}")
        print(f"  Таймаут: {self.api_timeout} сек")
        print()

        # UI настройки
        print("🌐 UI Настройки:")
        print(f"  Базовый URL: {self.base_url}")
        print(f"  Драйвер: {self.browser}")
        print(f"  Окно: {self.window_width}x{self.window_height}")
        print(f"  Headless: {'Да' if self.headless else 'Нет'}")
        print()

        # Таймауты
        print("⏱️  Таймауты:")
        print(f"  Ожидание элементов: {self.wait_timeout} сек")
        print(f"  Загрузка страницы: {self.driver_page_load_timeout} сек")
        print(f"  Капча: {self.captcha_wait_time} сек")
        print()

        # Директории
        print("📁 Директории:")
        print(f"  Скриншоты: {self.screenshots_dir}")
        print(f"  Логи: {self.logs_dir}")
        print(f"  Тестовые данные: {self.test_data_dir}")
        print(f"  Allure результаты: {self.allure_results_dir}")
        print()

        # Предупреждения
        warnings = []
        if not self.api_key:
            warnings.append("API_KEY не установлен. API тесты могут не работать.")

        if warnings:
            print("⚠️  Предупреждения:")
            for warning in warnings:
                print(f"  • {warning}")
            print()

        print("✅ Конфигурация корректна")
        print("=" * 60)

    def __str__(self) -> str:
        """Строковое представление настроек."""
        lines = [
            "Настройки тестов Кинопоиск:",
            f"  API URL: {self.api_url}",
            f"  API Key: {'***' + self.api_key[-4:] if self.api_key else 'Нет'}",
            f"  Base URL: {self.base_url}",
            f"  Browser: {self.browser}",
            f"  Headless: {self.headless}",
            f"  Window: {self.window_width}x{self.window_height}",
        ]
        return "\n".join(lines)


# Создание глобального экземпляра настроек
settings = Settings()


def print_config_summary():
    """Печать сводки конфигурации."""
    settings.print_config_summary()


# Алиасы для обратной совместимости (включая старые имена)
API_URL = settings.api_url
API_KEY = settings.api_key
BASE_URL = settings.base_url
BROWSER = settings.browser
HEADLESS = settings.headless
IS_API_CONFIGURED = settings.is_api_configured
API_HEADERS = settings.api_headers

# Для совместимости со старым кодом
EXPLICIT_WAIT = settings.wait_timeout
WAIT_TIMEOUT = settings.wait_timeout
DRIVER_NAME = settings.browser
WINDOW_HEADLESS = settings.headless
LOG_LEVEL = settings.log_level

__all__ = [
    "settings",
    "Settings",
    "print_config_summary",
    "API_URL",
    "API_KEY",
    "BASE_URL",
    "BROWSER",
    "HEADLESS",
    "IS_API_CONFIGURED",
    "API_HEADERS",
    "EXPLICIT_WAIT",
    "WAIT_TIMEOUT",
    "DRIVER_NAME",
    "WINDOW_HEADLESS",
    "LOG_LEVEL",
]