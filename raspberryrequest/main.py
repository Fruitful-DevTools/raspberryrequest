from typing import Dict, Literal
import requests
import time
from requests import ReadTimeout, Timeout, HTTPError

from raspberryrequest.components import make_request
from raspberryrequest.modules import calculate_backoff, valid_status
from raspberryrequest.exceptions import FatalStatusCodeError, MaxRetryError


class APIRequestHandler:
    attempt_number: int

    def __init__(self, headers: Dict[str, str] = None, max_retry_attempts: int = 3):
        """
        Initializes the API Request Handler.

        Args:
            headers: The headers to be included in the API requests.
            max_retry_attempts: The maximum number of retry attempts for failed requests.
        """
        self.headers = headers or {}
        self.max_retry_attempts = max_retry_attempts
        self.session = requests.Session()

    def send_api_request(
            self,
            base_url: str,
            method: Literal['GET', 'POST'] = 'GET',
            params: Dict[str, str] = None,
            data: Dict[str, str] = None,
            headers: Dict[str, str] = None) -> Dict:
        """
        Sends an API request with retry logic.

        Args:
            base_url: The base URL of the API.
            method: The HTTP method of the request (GET or POST).
            params: The query parameters to be included in the request.
            data: The request body data.
            headers: The headers to be included in the request.

        Returns:
            The response JSON data as a dictionary, if the request is successful.

        Raises:
            FatalStatusCodeError: If a fatal status code is received.
        """
        headers = headers or self.headers
        self.attempt_number = 1

        try:
            while self.attempt_number <= self.max_retry_attempts:
                try:
                    response = make_request(
                        base_url, method, headers, params, data, self.session)
                    if valid_status(response):
                        return response.json()
                    self.backoff()
                except (ReadTimeout, Timeout, HTTPError):
                    self.backoff()
                except FatalStatusCodeError as exc:
                    self.session.close()
                    raise FatalStatusCodeError() from exc
        finally:
            self.session.close()

    def backoff(self):
        """
        Implements backoff logic between retry attempts.
        """
        if self.attempt_number >= self.max_retry_attempts:
            raise MaxRetryError

        delay = calculate_backoff(self.attempt_number)
        time.sleep(delay)
        self.attempt_number += 1
