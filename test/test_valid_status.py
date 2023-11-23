import unittest
from unittest.mock import Mock
from raspberryrequest.validate import valid_status
from raspberryrequest.exceptions import NonRetryableStatusCodeError, FatalStatusCodeError
from raspberryrequest.config import StatusCodes
import requests


class TestValidStatus(unittest.TestCase):

    def setUp(self):
        self.status_codes = StatusCodes()

    def test_valid_status_valid_status(self):

        # Create a mock Response object with a valid status code
        response = requests.Response()
        response.status_code = 200
        response.reason = "test"

        # The function should return True for valid statuses
        result = valid_status(response, self.status_codes)
        self.assertTrue(result)

    def test_valid_status_retryable_status(self):
        # Create a mock Response object with a retryable status code
        response = requests.Response()
        response.status_code = 429
        response.reason = "test"

        # The function should return False for retryable statuses
        result = valid_status(response, self.status_codes)
        self.assertFalse(result)

    def test_valid_status_non_retryable_status(self):
        # Create a mock Response object with a non-retryable status code
        response = requests.Response()
        response.status_code = 308
        response.reason = "test"

        # The function should raise a NonRetryableStatusCodeError
        with self.assertRaises(NonRetryableStatusCodeError) as context:
            valid_status(response, self.status_codes)

        # Check that the error message is as expected
        self.assertIn("Cannot retry. Non-retryable status: 308",
                      str(context.exception))

    def test_valid_status_fatal_status(self):
        # Create a mock Response object with a fatal status code
        response = requests.Response()
        response.status_code = 403
        response.reason = "test"

        # The function should raise a FatalStatusCodeError
        with self.assertRaises(FatalStatusCodeError) as context:
            valid_status(response, self.status_codes)

        # Check that the error message is as expected
        self.assertIn(
            "Fatal status code: 403. Raspberry request will stop.", str(context.exception))


if __name__ == '__main__':
    unittest.main()
