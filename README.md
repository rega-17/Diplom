# Проект автотестов для Кинопоиска

## Описание проекта

Автоматизированные тесты для веб-сайта Кинопоиск и его API. Проект включает UI и API тесты для проверки функциональности платформы.

## Предварительные требования

- Установить Python 3.8+
- Установить Chrome браузер (последняя версия)
- Получить API ключ Кинопоиска (на api.kinopoisk.dev)

## Установка

1. Установить зависимости:

pip install -r requirements.txt

2 Создать файл .env на основе .env.example:
copy .env.example .env

3 Настроить .env файл:
API_URL=https://api.kinopoisk.dev/v1.4
KINOPOISK_API_KEY=ваш_ключ_здесь
BASE_URL=https://www.kinopoisk.ru
BROWSER=chrome
HEADLESS=false

 Режимы запуска тестов
1 Запустить только UI тесты
pytest -v -m ui

2 Запустить только API тесты
pytest -v -m api

3 Запустить все тесты
pytest -v

Запустить тесты с генерацией Allure отчета

pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report

Структура проекта

Diplom/
├── config/
├── pages/
├── test/
├── utils/
├── .env
├── .env.example
├── pytest.ini
├── requirements.txt
└── README.md

Тестовые сценарии
UI тесты

1 Проверить доступность поля поиска

2 Проверить очистку поля поиска

3 Проверить переходы по ссылкам актеров

4 Проверить кнопку "Назад"

5 Проверить подсказку максимальной длины отзыва

API тесты

1 Найти фильм по кириллическому названию

2 Найти фильм по цифровому названию

3 Найти фильм по латинскому названию

4 Проверить негативный поиск несуществующего фильма

5 Проверить поиск фильма с датой из будущего

6 Получить информацию о фильме по ID

7 Проверить пагинацию


Конфигурация
Проверить настройки

python -c "from config import settings; settings.print_config_summary()"

Устранение проблем
-API_KEY не установлен
-Убедиться что файл .env существует
-Проверить корректность API ключа
-Ошибки WebDriver
-Убедиться что Chrome установлен
-Попробовать запустить с HEADLESS=false
-Ошибки импорта
-Проверить установку зависимостей
-Запустить pip install -r requirements.txt

Ссылки
Финальный проект по ручному тестированию: [ https://disk.yandex.ru/i/6rNMug1Ohknafw]

API документация Кинопоиска: https://api.kinopoisk.dev

Официальный сайт Кинопоиска: https://www.kinopoisk.ru

Проект выполнен: Галеева Резеда Рубисовна