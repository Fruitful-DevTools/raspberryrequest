
class StatusCodes:
    valid_statuses = {200, 201}
    retryable_statuses = {408, 429, 500, 502, 503, 504}
    non_retryable_statuses = {308, 400, 401, 404}
    fatal_statuses = {403}
