"""
Module: backoff_calculator

This module provides a function for calculating backoff time for retrying operations,
especially in the context of handling failed HTTP requests marked as "retryable."

Functions:
----------
- `calculate_backoff`(attempt_number: int, max_delay: int = 10) -> float:
    Calculates the backoff time based on the attempt number and
    a specified maximum delay.

Usage:
------
    This module can be imported and used in scenarios where
    backoff is needed to manage retries for operations, such as
    when dealing with retryable HTTP requests.

Example:
--------
    ```python
    import backoff_calculator

    # Use the calculate_backoff function
    attempts = 3
    max_delay = 10
    backoff_time = backoff_calculator.calculate_backoff(attempt_number=3, max_delay=10)
    ```
"""
import random


def calculate_backoff(attempt_number: int, max_delay: int = 10) -> float:
    """
    Calculates the backoff time for retrying an operation.
    Backoff is ran when a HTTP request fails, and the code is
    defined as "retryable".

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
