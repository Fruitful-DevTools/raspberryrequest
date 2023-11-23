import requests
import logging
from raspberryrequest.config import StatusCodes
from raspberryrequest.exceptions import NonRetryableStatusCodeError, FatalStatusCodeError

logging.basicConfig(
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('proxypull.log')]
)


def valid_status(response: requests.Response, status_codes: StatusCodes) -> bool:
    """
    Check if the response status code is valid based on the given
    status codes.

    - :param `response`: The response object to check.
    - :type `response`: `requests.Response`
    - :param `status_codes`: The status codes to check against.
    - :type `status_codes`: `StatusCodes`
    - :return: `True` if the response status code is valid, `False` otherwise.
    - :rtype: `bool`
    """
    code = response.status_code

    if not code:
        logging.warning('No response status code.')
        return False

    if code in status_codes.VALID:
        return True
    if code in status_codes.RETRYABLE:
        return False
    if code in status_codes.NONRETRYABLE:
        raise NonRetryableStatusCodeError(
            f'Cannot retry. Non-retryable status: {code}')
    if code in status_codes.FATAL:
        raise FatalStatusCodeError(
            f'Fatal status code: {code}. Raspberry request will stop.')

    return False
