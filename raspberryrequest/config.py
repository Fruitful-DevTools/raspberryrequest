from dataclasses import dataclass


@dataclass
class StatusCodes:

    VALID = [200, 201]
    RETRYABLE = [408, 429, 500, 502, 503, 504]
    NONRETRYABLE = [308, 400, 401, 404]
    FATAL = [403]

    def __repr__(self):
        return f"Valid: {self.VALID} \n Retryable: {self.RETRYABLE} \n NonRetryable: {self.NONRETRYABLE} \n Fatal: {self.FATAL}"
