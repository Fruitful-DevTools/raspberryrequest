import random


def calculate_backoff(attempt_number: int, max_delay: int = 10) -> float:
    """
    Calculates the backoff time for retrying an operation.

    Args:
    -----
    - `attempt_number` (`int`): The number of attempts made so 
    far.
    - `max_delay` (`int, optional`): The maximum delay allowed
    for backoff. Defaults to 10.

    Returns:
    --------
    - `float`: The calculated backoff time.

    Note:
    -----
    - The backoff time is calculated using an exponential
    function with a random factor.
    - The delay is calculated as 2 raised to the power of the
    attempt number.
    - The delay is then capped at the maximum delay specified.
    - The backoff time is calculated by multiplying the capped
    delay with a random factor between 1 and 2.
    """
    delay = 2 ** attempt_number
    capped_delay = min(delay, max_delay)
    backoff = capped_delay * (1 + random.random())
    return backoff
