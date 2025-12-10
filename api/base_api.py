import requests
import allure
import logging
from typing import Any, Dict, Optional, Union


class BaseAPI:
    """Базовый класс для работы с API."""
    
    def __init__(self, base_url: str = None, headers: Dict[str, str] = None):
        """
        Инициализация базового API клиента.
        
        Args:
            base_url: Базовый URL API
            headers: Заголовки запросов
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Настраиваем сессию
        if self.headers:
            self.session.headers.update(self.headers)
    
    @allure.step("Отправка GET запроса")
    def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Отправляет GET запрос.
        
        Args:
            endpoint: Эндпоинт API
            params: Параметры запроса
            **kwargs: Дополнительные аргументы для requests
            
        Returns:
            Объект Response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
        
        self.logger.info(f"GET запрос: {url}")
        self.logger.debug(f"Параметры: {params}")
        
        try:
            response = self.session.get(url, params=params, **kwargs)
            self._log_response(response)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка при GET запросе к {url}: {e}")
            raise
    
    @allure.step("Отправка POST запроса")
    def post(
        self, 
        endpoint: str, 
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Отправляет POST запрос.
        
        Args:
            endpoint: Эндпоинт API
            data: Данные для отправки (form-encoded)
            json: JSON данные для отправки
            **kwargs: Дополнительные аргументы для requests
            
        Returns:
            Объект Response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
        
        self.logger.info(f"POST запрос: {url}")
        self.logger.debug(f"Данные: {data or json}")
        
        try:
            response = self.session.post(url, data=data, json=json, **kwargs)
            self._log_response(response)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка при POST запросе к {url}: {e}")
            raise
    
    def _log_response(self, response: requests.Response) -> None:
        """Логирует информацию о ответе."""
        self.logger.info(f"Статус ответа: {response.status_code}")
        self.logger.debug(f"Заголовки ответа: {dict(response.headers)}")
        
        # Логируем тело ответа только если оно не слишком большое
        try:
            if response.text and len(response.text) < 1000:
                self.logger.debug(f"Тело ответа: {response.text}")
        except:
            pass
    
    @allure.step("Проверка статус кода ответа")
    def assert_status_code(
        self, 
        response: requests.Response, 
        expected_code: int = 200
    ) -> None:
        """
        Проверяет статус код ответа.
        
        Args:
            response: Объект Response
            expected_code: Ожидаемый статус код
            
        Raises:
            AssertionError: Если статус код не соответствует ожидаемому
        """
        actual_code = response.status_code
        assert actual_code == expected_code, \
            f"Неверный статус код. Ожидалось: {expected_code}, получено: {actual_code}"
        
        self.logger.info(f"Статус код корректен: {actual_code}")
    
    @allure.step("Проверка JSON ответа")
    def assert_json_contains(
        self, 
        response: requests.Response, 
        expected_key: str, 
        expected_value: Any = None
    ) -> Dict[str, Any]:
        """
        Проверяет что JSON ответ содержит определённый ключ (и значение).
        
        Args:
            response: Объект Response
            expected_key: Ожидаемый ключ в JSON
            expected_value: Ожидаемое значение (если None, проверяется только наличие ключа)
            
        Returns:
            Распарсенный JSON
            
        Raises:
            AssertionError: Если ключ не найден или значение не совпадает
        """
        try:
            json_data = response.json()
        except ValueError as e:
            self.logger.error(f"Не удалось распарсить JSON: {e}")
            raise AssertionError(f"Ответ не является валидным JSON: {response.text}")
        
        assert expected_key in json_data, \
            f"Ключ '{expected_key}' не найден в ответе. Доступные ключи: {list(json_data.keys())}"
        
        if expected_value is not None:
            actual_value = json_data[expected_key]
            assert actual_value == expected_value, \
                f"Неверное значение для ключа '{expected_key}'. " \
                f"Ожидалось: {expected_value}, получено: {actual_value}"
        
        self.logger.info(f"JSON содержит ключ '{expected_key}'")
        return json_data