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
from .config import StatusCodes

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
        Initializes the `APIRequestHandler`.

        :param headers: The headers to be included in the
        API requests.
        :type headers: Dict[str, str]
        :param max_attempts: The maximum number of retry
        attempts for failed requests.
        :type max_attempts: int
        :param max_delay: The maximum delay allowed for
        backoff.
        :type max_delay: int
        """
        self.headers = headers or {}
        self.max_attempts = max_attempts
        self.max_delay = max_delay

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.status_codes = StatusCodes()

    def send_api_request(
            self,
            base_url: str,
            method: Literal['GET', 'POST'] = 'GET',
            params: Dict[str, str] = None,
            headers: Dict[str, str] = None) -> Dict:
        """
        Sends an API request with retry logic.

        :param base_url: The base URL of the API.
        :type base_url: str
        :param method: The HTTP method of the request
        :type method: Literal['GET', 'POST']
        :param params: The query parameters to be included in the
        request.
        :type params: Dict[str, str]
        :param headers: The headers to be included in the request.
        :type headers: Dict[str, str]
        :return: The JSON response from the API.
        :rtype: Dict
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
                if valid_status(response, self.status_codes):
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

    def add_status_code(self,
                        status_list_name: Literal['VALID',
                                                  'RETRYABLE',
                                                  'NONRETRYABLE',
                                                  'FATAL'],
                        status_code: int):
        """
        Adds a status code to a specified status list.

        - :param `status_list_name`: The name of the status list to
        add the status code to.
        - :type `status_list_name`: Literal[`'VALID'`, `'RETRYABLE'`,
        `'NONRETRYABLE'`, `'FATAL'`]
        - :param `status_code`: The status code to add.
        - :type `status_code`: `int`
        """
        status_list = getattr(self.status_codes, status_list_name)
        if status_code not in status_list:
            status_list.append(status_code)

    def remove_status_code(self,
                           status_list_name: Literal['VALID',
                                                     'RETRYABLE',
                                                     'NONRETRYABLE',
                                                     'FATAL'],
                           status_code: int):
        """
        Remove a status code from the specified status list.

        - :param `status_list_name`: The name of the status list to
        add the status code to.
        - :type `status_list_name`: Literal[`'VALID'`, `'RETRYABLE'`,
        `'NONRETRYABLE'`, `'FATAL'`]
        - :param `status_code`: The status code to add.
        - :type `status_code`: `int`
        """
        status_list = getattr(self.status_codes, status_list_name)
        status_list.remove(status_code)

    def get_status_codes(self):
        """
        Get the status codes.

        :return: The status codes.
        :rtype: `StatusCodes`
        """
        return self.status_codes

    def print_status_codes(self):
        """
        Print the status codes.

        This method prints the status codes stored in the
        `status_codes` attribute of the `APIRequestHandler`
        object.
        """
        print(self.status_codes)

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

    @property
    def calls(self):
        """
        Returns the number of calls made in the current session.
        """
        return self.call_number
