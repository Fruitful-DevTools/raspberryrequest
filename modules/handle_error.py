import logging
from models import StatusCodes
from exceptions import FatalStatusCode, UnusableStatusCode
import requests


def handle_error(response: requests.Response) -> None:
    try:
        if response.status_code in StatusCodes.non_retryable_statuses:
            logging.info('Non-retryable status:%s', response.status_code)
            raise UnusableStatusCode()
        if response.status_code in StatusCodes.fatal_statuses:
            logging.critical('Fatal status code received.')
            raise FatalStatusCode()
    except AttributeError:
        pass
