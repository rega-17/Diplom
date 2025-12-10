import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config.settings import settings
import os


def create_simple_driver():
    """Создаёт упрощённый Chrome драйвер."""
    
    options = Options()
    
    if settings.headless:
        options.add_argument("--headless")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    
    # Пробуем разные способы создания драйвера
    try:
        # Способ 1: Автоматический (если chromedriver в PATH)
        driver = webdriver.Chrome(options=options)
        allure.attach("Драйвер создан автоматически", name="Driver Info")
        return driver
    except Exception as e1:
        allure.attach(f"Ошибка автосоздания: {e1}", name="Driver Error")
        
        try:
            # Способ 2: Явный путь (если chromedriver.exe в папке проекта)
            if os.path.exists("chromedriver.exe"):
                service = Service(executable_path="chromedriver.exe")
                driver = webdriver.Chrome(service=service, options=options)
                allure.attach("Драйвер создан из chromedriver.exe в папке проекта", name="Driver Info")
                return driver
        except Exception as e2:
            allure.attach(f"Ошибка с явным путём: {e2}", name="Driver Error")
        
        # Способ 3: Скачиваем вручную
        print("\n" + "="*60)
        print("❌ ChromeDriver не найден!")
        print("="*60)
        print("Сделай следующее:")
        print("1. Открой: https://chromedriver.chromium.org/")
        print("2. Скачай версию для Windows")
        print("3. Распакуй chromedriver.exe в папку проекта")
        print("4. Запусти тесты снова")
        print("="*60)
        
        # Создаём файл-инструкцию
        with open("HOW_TO_INSTALL_CHROMEDRIVER.txt", "w", encoding="utf-8") as f:
            f.write("Инструкция по установке ChromeDriver:\n")
            f.write("1. Перейди: https://chromedriver.chromium.org/\n")
            f.write("2. Нажми 'Latest stable release'\n")
            f.write("3. Скачай 'chromedriver_win32.zip'\n")
            f.write("4. Распакуй chromedriver.exe\n")
            f.write("5. Помести chromedriver.exe в папку проекта\n")
            f.write("6. Запусти тесты снова\n")
        
        raise Exception("ChromeDriver не установлен. Следуй инструкции в файле HOW_TO_INSTALL_CHROMEDRIVER.txt")