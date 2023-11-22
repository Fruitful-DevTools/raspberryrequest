import logging
from typing import Dict, Literal
import requests
import time
from requests import ReadTimeout, Timeout, HTTPError

from .exceptions import (FatalStatusCodeError, MaxRetryError,
                         NonRetryableStatusCodeError)
from .backoff import calculate_backoff
from .validate import valid_status
from .request import make_request

logger = logging.basicConfig(
    level=logging.WARNING,
    format=' %(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(),
              logging.FileHandler('proxypull.log')]
)


class APIRequestHandler:
    call_number = 0

    def __init__(self, headers: Dict[str, str] = None,
                 max_attempts: int = 3, max_delay: int = 10):
        """
        Initializes the API Request Handler.

        Args:
        -----
        - `headers` (`dict`): The headers to be included in the
        API requests.
        - `max_attempts` (`int`): The maximum number of retry
        attempts for failed requests.
        - `max_delay` (`int`): The maximum delay allowed for
        backoff.
        """
        self.headers = headers or {}
        self.max_attempts = max_attempts
        self.max_delay = max_delay
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def send_api_request(
            self,
            base_url: str,
            method: Literal['GET', 'POST'] = 'GET',
            params: Dict[str, str] = None,
            headers: Dict[str, str] = None) -> Dict:
        """
        Sends an API request with retry logic.

        Args:
        -----
        - `base_url`: The base URL of the API.
        - `method`: The HTTP method of the request (`GET` or
        `POST`).
        - `params`: The query parameters to be included in the
        request.
        - `headers`: The headers to be included in the request.

        Returns:
        --------
        - The response JSON data as a dictionary, if the request
        is successful.

        Raises:
        -------
        - `FatalStatusCodeError`: If a fatal status code is received.
        """
        headers = headers or self.headers

        while self.call_number <= self.max_attempts:
            try:
                self.call_number += 1
                response = make_request(
                    base_url, method, headers, params, self.session)
            except (ReadTimeout, Timeout, HTTPError):
                self._backoff(base_url, method, params, headers)

            try:
                if valid_status(response):
                    return response.json()
            except NonRetryableStatusCodeError:
                return None
            except FatalStatusCodeError:
                self.close_session()
                raise FatalStatusCodeError()

            self._backoff(base_url, method, params, headers)

    def close_session(self):
        """
        Closes the current session.

        This function resets the call number to 0 and closes the
        session.
        """
        self.call_number = 0
        self.session.close()

    @property
    def calls(self):
        """
        Returns the number of calls made in the current session.
        """
        return self.call_number

    def _backoff(self, base_url: str,
                 method: Literal['GET', 'POST'] = 'GET',
                 params: Dict[str, str] = None,
                 headers: Dict[str, str] = None) -> None:

        if self.call_number < self.max_attempts:
            delay = calculate_backoff(self.call_number)
            time.sleep(delay)
            self.send_api_request(base_url, method, params,
                                  headers)
        else:
            raise MaxRetryError("Max retry attempts reached.")
