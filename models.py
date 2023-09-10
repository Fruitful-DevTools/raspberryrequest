
class StatusCodes:
    def __init__(self):
        self.valid_statuses = {200, 201}
        self.retryable_statuses = {408, 429, 500, 502, 503, 504}
        self.non_retryable_statuses = {308, 400, 401, 404}
        self.fatal_statuses = {403}

    def add_valid_status(self, status):
        self.valid_statuses.add(status)

    def remove_valid_status(self, status):
        self.valid_statuses.remove(status)

    def add_retryable_status(self, status):
        self.retryable_statuses.add(status)

    def remove_retryable_status(self, status):
        self.retryable_statuses.remove(status)

    def add_non_retryable_status(self, status):
        self.non_retryable_statuses.add(status)

    def remove_non_retryable_status(self, status):
        self.non_retryable_statuses.remove(status)

    def add_fatal_status(self, status):
        self.fatal_statuses.add(status)

    def remove_fatal_status(self, status):
        self.fatal_statuses.remove(status)
