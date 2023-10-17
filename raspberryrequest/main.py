from .exceptions import FatalStatusCodeError, MaxRetryError, NonRetryableStatusCodeError
from .modules import calculate_backoff, valid_status
import logging
from typing import Dict, Literal
import requests
import time
from requests import ReadTimeout, Timeout, HTTPError

logger = logging.basicConfig(
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('proxypull.log')]
)


class APIRequestHandler:
    attempt_number: int

    def __init__(self, headers: Dict[str, str] = None, max_retry_attempts: int = 3):
        """
        Initializes the API Request Handler.

        Args:
            headers: The headers to be included in the API requests.
            max_retry_attempts: The maximum number of retry attempts for failed requests.
        """
        logging.info('Initializing APIRequestHandler...')
        self.headers = headers or {}
        self.max_retry_attempts = max_retry_attempts
        self.session = requests.Session()
        self.session.headers.update(self.headers)

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
                response = make_request(
                    base_url, method, headers, params, data, self.session)
                try:
                    if valid_status(response):
                        return response.json()
                except (ReadTimeout, Timeout, HTTPError):
                    logging.debug('Request error.')
                    self.backoff()
                except NonRetryableStatusCodeError:
                    logging.debug('Non-retryable status code.')
                    return None
                except FatalStatusCodeError as exc:
                    logging.warning('Fatal status code.')
                    self.session.close()
                    raise FatalStatusCodeError() from exc
                self.backoff()
        finally:
            logging.info('Closing session...')
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
