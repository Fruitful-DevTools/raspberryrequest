import random


def calculate_backoff(attempt_number: int, max_delay: int = 10) -> float:
    """
    Calculates the backoff time for retrying an operation.

    - :param `attempt_number`: The number of attempts made so far.
    - :type `attempt_number`: `int`
    - :param `max_delay`: The maximum delay allowed for backoff.
    - :type `max_delay`: `int`
    - :return: The calculated backoff time.
    - :rtype: `float`
    """
    delay = 2 ** attempt_number
    capped_delay = min(delay, max_delay)
    backoff = capped_delay * (1 + random.random())
    return backoff
