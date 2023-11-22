from dataclasses import dataclass


@dataclass
class StatusCall:
    def __init__(self, num, attempt):
        self.num = num
        self.attempt = attempt
