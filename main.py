
import time
from typing import Dict, Literal
from urllib3.exceptions import MaxRetryError

import requests
from requests import ReadTimeout, Timeout, HTTPError

from models import StatusCodes
from modules import calculate_backoff, handle_response, handle_error
from components import make_request


class RequestHandler:

    def __init__(self, headers: Dict[str, str] = None, max_retry_attempts: int = 3):
        self.headers = headers or {}
        self.max_retry_attempts = max_retry_attempts
        self.session = requests.Session()

    def send_request(
            self,
            base_url: str,
            method: Literal['GET', 'POST'] = 'GET',
            params: Dict[str, str] = None,
            data: Dict[str, str] = None,
            headers: Dict[str, str] = None) -> Dict:

        attempt_number = 1
        headers = headers or self.headers

        while attempt_number <= self.max_retry_attempts:
            try:
                response = make_request(
                    base_url, method, headers, params, data, self.session)
                if handle_response(response):
                    return response.json()
                else:
                    return None

            except (HTTPError, Timeout, ReadTimeout, MaxRetryError, ConnectionError, OSError) as e:
                if attempt_number == self.max_retry_attempts:
                    self.session.close()
                    raise e

                handle_error(response)
                delay = calculate_backoff(attempt_number)
                time.sleep(delay)
                attempt_number += 1

        self.session.close()
