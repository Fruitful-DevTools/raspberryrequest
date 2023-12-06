import logging
import sys
from typing import Dict, Literal
import requests
import time
from requests import ReadTimeout, Timeout, HTTPError

from .exceptions import (FatalStatusCodeError, MaxRetryError,
                         NonRetryableStatusCodeError)
from .backoff import calculate_backoff
from .validate import validate_status, update_session_data
from .request import make_request
from .models import SessionData, StatusCodes
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


class APIRequestHandler:
    call_number = 0

    def __init__(self, headers: Dict[str, str] = None,
                 max_attempts: int = 3, max_delay: int = 10, **kwargs):
        """
        Initializes an instance of the class.

        Parameters:
        -----------
        - :param `headers`: A dictionary of headers to be
        included in the requests made by the session.
        Defaults to None.
        - :type `headers`: `Dict[str, str]`
        - :param `max_attempts`: The maximum number of attempts
        to be made for each request. Defaults to 3.
        - :type `max_attempts`: int
        - :param `max_delay`: The maximum delay (in seconds)
        between attempts for each request. Defaults to 10.
        - :type `max_delay`: int
        - :param `**kwargs`: Additional keyword arguments:
            - :param `paid_status_codes`: A list of status codes
            that are considered "paid".
            - :type `paid_status_codes`: `List[int]`
        """
        self.headers = headers or {}
        self.max_attempts = max_attempts
        self.max_delay = max_delay

        self.session_data = SessionData()
        self.status_codes = StatusCodes()
        self.status_codes.PAID = kwargs.get('paid_status_codes', [])

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

        Parameters:
        -----------
        - :param `base_url`: The base URL of the API.
        - :type `base_url`: str
        - :param `method`: The HTTP method of the request
        - :type `method`: `Literal['GET', 'POST']`
        - :param `params`: The query parameters to be included in the
        request.
        - :type `params`: `Dict[str, str]`
        - :param `headers`: The headers to be included in the request.
        - :type `headers`: `Dict[str, str]`

        Returns:
        --------
        - :return: The JSON response from the API.
        - :rtype: `Dict`

        Raises:
        -------
        - :raises `MaxRetryError`: If the maximum number of attempts.
        has been reached.
        - :raises `NonRetryableStatusCodeError`: If the status code
        is not in the list of retryable status codes.
        - :raises `FatalStatusCodeError`: If the status code is
        in the list of fatal status codes.
        -------------------------------------------

        Example:
        --------
        ```python
        from raspberryrequest import APIRequestHandler
        headers = {"Content-Type": "application/json"}
        max_attempts = 3
        max_delay = 10

        # Set paid status codes
        # List of status codes that are charged for by the API.
        paid_status_codes = [200, 201, 260]

        handler = APIRequestHandler(headers=headers,
                                    max_attempts=max_attempts,
                                    max_delay=max_delay,
                                    paid_status_codes=paid_status_codes)

        response = handler.send_api_request(base_url="https://example.com", 
        method="GET", params={"param1": "value1"}, headers=headers)

        print(response)
        # {'example': 'response'}
        ```
        """
        logger.debug("Call number: %s", self.call_number)
        headers = headers or self.headers

        while self.call_number <= self.max_attempts:
            try:
                self.call_number += 1
                logger.debug("Call number: %s", self.call_number)
                logger.debug("max attempts: %s", self.max_attempts)
                response = make_request(
                    base_url, method, headers, params, self.session)
                status_code = response.status_code
            except (ReadTimeout, Timeout, HTTPError):
                logger.debug("ReadTimeout, Timeout, HTTPError")
                self._backoff(base_url, method, params, headers)

            try:
                self.session_data = update_session_data(
                    status_code, self.status_codes, self.session_data)
                if validate_status(status_code, self.status_codes):
                    return response.json()
            except NonRetryableStatusCodeError:
                logger.debug("NonRetryableStatusCodeError")
                return None
            except FatalStatusCodeError:
                logger.debug("FatalStatusCodeError")
                self.close_session()
                raise FatalStatusCodeError()

            self._backoff(base_url, method, params, headers)

    def close_session(self):
        """
        Closes the current session.

        This function resets the call number to 0 and closes the
        session.
        """
        logger.debug("Closing session")
        self.call_number = 0
        self.session_data.reset()
        self.session.close()
        logger.debug("Session closed")

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
        logger.debug("Adding status code: %s", status_code)
        status_list = getattr(StatusCodes, status_list_name)
        if status_code not in status_list:
            logger.debug("Status code added: %s", status_code)
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
        logger.debug("Removing status code: %s", status_code)
        status_list = getattr(self.status_codes, status_list_name)
        status_list.remove(status_code)
        logger.debug("Status code removed: %s", status_code)

    def get_status_codes(self):
        """
        Get the status codes.

        Returns:
        --------
        - :return: The status codes.
        - :rtype: `StatusCodes`
        """
        logger.debug("Getting status codes")
        return self.status_codes

    def print_status_codes(self):
        """
        Print the status codes.

        This method prints the status codes stored in the
        `status_codes` attribute of the `APIRequestHandler`
        object.
        """
        logger.debug("Printing status codes")
        print(StatusCodes)

    def get_session_data(self):
        """
        Return the session data as a dictionary.

        :return: A dictionary containing the session data.
        """
        logger.debug("Getting session data")
        return self.session_data.get_dict()

    def _backoff(self, base_url: str,
                 method: Literal['GET', 'POST'] = 'GET',
                 params: Dict[str, str] = None,
                 headers: Dict[str, str] = None) -> None:
        logger.debug("Backing off")
        if self.call_number < self.max_attempts:
            delay = calculate_backoff(self.call_number)
            logger.debug("Delay: %s", delay)
            time.sleep(delay)
            logger.debug("Sending API request")
            self.send_api_request(base_url, method, params,
                                  headers)
        else:
            logger.debug("Max retry attempts reached.")
            raise MaxRetryError("Max retry attempts reached.")

    @property
    def calls(self):
        """
        Returns the number of calls made in the current session.
        """
        return self.call_number
