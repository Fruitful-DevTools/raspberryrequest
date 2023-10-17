import random


def calculate_backoff(attempt_number: int) -> float:
    delay = min(2 ** attempt_number, 10)
    jitter = random.uniform(0, 1)
    return delay * (1 + jitter)
