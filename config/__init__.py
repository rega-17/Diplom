
"""
Пакет конфигурации тестов Кинопоиска.
"""

# Реэкспорт настроек
from .settings import (
    settings,
    Settings,
    print_config_summary,
    API_URL,
    API_KEY,
    BASE_URL,
    BROWSER,
    HEADLESS,
    IS_API_CONFIGURED,
    API_HEADERS,
    EXPLICIT_WAIT,
    WAIT_TIMEOUT,
    DRIVER_NAME,
    WINDOW_HEADLESS,
    LOG_LEVEL,
)

__all__ = [
    'settings',
    'Settings',
    'print_config_summary',
    'API_URL',
    'API_KEY',
    'BASE_URL',
    'BROWSER',
    'HEADLESS',
    'IS_API_CONFIGURED',
    'API_HEADERS',
    'EXPLICIT_WAIT',
    'WAIT_TIMEOUT',
    'DRIVER_NAME',
    'WINDOW_HEADLESS',
    'LOG_LEVEL',
]