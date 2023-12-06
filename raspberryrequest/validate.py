import logging
import sys
from .exceptions import NonRetryableStatusCodeError, FatalStatusCodeError
from .models import SessionData, StatusCodes
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


status_code = StatusCodes()


def update_session_data(code: int, status_codes: StatusCodes,
                        session_data: SessionData) -> SessionData:
    """
    Update the session data based on the given code and status
    codes.

    Parameters:
    -----------
    - `code`: An integer representing the code.
    - `status_codes`: An instance of the `StatusCodes` class.
    - `session_data`: An instance of the `SessionData` class.

    Returns:
    --------
    - The updated session data.
    """
    session_data.PAID += code in status_codes.PAID
    logger.debug('PAID: %s', session_data.PAID)
    session_data.UNPAID += code not in status_codes.PAID
    logger.debug('UNPAID: %s', session_data.UNPAID)
    session_data.VALID += code in status_codes.VALID
    logger.debug('VALID: %s', session_data.VALID)
    session_data.RETRYABLE += code in status_codes.RETRYABLE
    logger.debug('RETRYABLE: %s', session_data.RETRYABLE)
    session_data.NONRETRYABLE += code in status_codes.NONRETRYABLE
    logger.debug('NONRETRYABLE: %s', session_data.NONRETRYABLE)
    session_data.FATAL += code in status_codes.FATAL
    logger.debug('FATAL: %s', session_data.FATAL)
    return session_data


def validate_status(code, status_codes: StatusCodes) -> bool:
    """
    Validate the status code against a set of predefined status
    codes.

    - :param `code`: The status code to be validated.
    - :param `status_codes`: An object containing the predefined
    status codes.
    - :type `code`: `int`
    - :type `status_codes`: `StatusCodes`

    Returns:
    --------
    - :return: True if the code is valid, False otherwise.
    - :rtype: `bool`

    Raises:
    --------
    - :raises `NonRetryableStatusCodeError`: If the code is not in
    `NONRETRYABLE` status codes.
    - :raises `FatalStatusCodeError`: If the code is in the `FATAL`
    status codes.
    """

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
