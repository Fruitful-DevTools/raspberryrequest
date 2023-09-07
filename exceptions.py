from typing import Optional


class StatusCodeError(Exception):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Error in status code.')


class UnusableStatusCode(StatusCodeError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Unusable status code.')


class FatalStatusCode(StatusCodeError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Fatal status code. Raspberry request will stop.')
