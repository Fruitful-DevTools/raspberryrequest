
class StatusCodes:
    valid_statuses = {200, 201}
    non_retryable_statuses = {400, 401, 404, 500, 503}
    fatal_statuses = {403}
