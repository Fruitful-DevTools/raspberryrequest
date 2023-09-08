import requests

from exceptions import NonRetryableStatusCodeError, FatalStatusCodeError
from models import StatusCodes


def valid_status(response: requests.Response) -> bool:
    if response.status_code in StatusCodes.valid_statuses:
        return True
    elif response.status_code in StatusCodes.retryable_statuses:
        return False
    elif response.status_code in StatusCodes.non_retryable_statuses:
        raise NonRetryableStatusCodeError(
            f'Cannot retry. Non-retryable status: {response.status_code}')
    elif response.status_code in StatusCodes.fatal_statuses:
        raise FatalStatusCodeError(
            f'Fatal status code: {response.status_code}. Raspberry request will stop.')
    return False
