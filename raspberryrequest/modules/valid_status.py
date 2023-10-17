import requests

from raspberryrequest.exceptions import NonRetryableStatusCodeError, FatalStatusCodeError
from raspberryrequest.models import StatusCodes

codes = StatusCodes()


def valid_status(response: requests.Response) -> bool:
    if response.status_code in codes.valid_statuses:
        return True
    elif response.status_code in codes.retryable_statuses:
        return False
    elif response.status_code in codes.non_retryable_statuses:
        raise NonRetryableStatusCodeError(
            f'Cannot retry. Non-retryable status: {response.status_code}')
    elif response.status_code in codes.fatal_statuses:
        raise FatalStatusCodeError(
            f'Fatal status code: {response.status_code}. Raspberry request will stop.')
    return False
