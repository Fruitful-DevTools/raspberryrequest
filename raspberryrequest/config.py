

from typing import Any


class StatusCodes:

    VALID = [200, 201]
    RETRYABLE = [408, 429, 500, 502, 503, 504]
    NONRETRYABLE = [308, 400, 401, 404]
    FATAL = [403]
