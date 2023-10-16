from typing import Optional


class RaspberryRequestError(Exception):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Error in RaspberryRequest.')


class MaxRetryError(RaspberryRequestError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Maximum number of request retries reached.')


class StatusCodeError(RaspberryRequestError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Error in status code.')


class NonRetryableStatusCodeError(StatusCodeError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Unusable status code.')


class FatalStatusCodeError(StatusCodeError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Fatal status code. Raspberry request will stop.')
