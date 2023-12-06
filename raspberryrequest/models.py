from dataclasses import dataclass


@dataclass
class SessionData:
    VALID = 0
    RETRYABLE = 0
    NONRETRYABLE = 0
    FATAL = 0
    PAID = 0
    UNPAID = 0
    TOTAL = 0

    def __repr__(self):
        return "VALID: {}\nRETRYABLE: {}\nNONRETRYABLE: {}\nFATAL: {}\nPAID: {}\nUNPAID: {}\nTOTAL: {}".format(
            self.VALID, self.RETRYABLE, self.NONRETRYABLE, self.FATAL, self.PAID, self.UNPAID, self.TOTAL
        )

    def reset(self):
        """
        Reset all the `SessionData` attributes to their initial
        values.
        """
        self.VALID, self.RETRYABLE, self.NONRETRYABLE, self.FATAL, self.PAID, self.UNPAID, self.TOTAL = 0, 0, 0, 0, 0, 0, 0

    def update_total(self):
        """
        Updates the total call count by summing the values of
        `VALID`, `RETRYABLE`, `NONRETRYABLE`, and `FATAL`.
        """
        self.TOTAL = sum([
            self.VALID,
            self.RETRYABLE,
            self.NONRETRYABLE,
            self.FATAL
        ])

    def get_dict(self):
        return {
            'VALID': self.VALID,
            'RETRYABLE': self.RETRYABLE,
            'NONRETRYABLE': self.NONRETRYABLE,
            'FATAL': self.FATAL,
            'TOTAL': self.TOTAL,
            'PAID': self.PAID,
            'UNPAID': self.UNPAID
        }


@dataclass
class StatusCodes:

    VALID = [200, 201]
    RETRYABLE = [408, 429, 500, 502, 503, 504]
    NONRETRYABLE = [308, 400, 401, 404]
    FATAL = [403]
    PAID = []

    def __repr__(self):
        return f"Valid: {self.VALID} \n Retryable: {self.RETRYABLE} \n NonRetryable: {self.NONRETRYABLE} \n Fatal: {self.FATAL}"
