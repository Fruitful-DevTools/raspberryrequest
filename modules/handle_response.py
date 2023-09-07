import requests
from requests import HTTPError

from models import StatusCodes


def handle_response(response: requests.Response) -> bool:
    if response.status_code in StatusCodes.valid_statuses:
        return True
    elif not response.status_code in StatusCodes.non_retryable_statuses:
        raise HTTPError(response.content.decode('utf-8'))
    return False
