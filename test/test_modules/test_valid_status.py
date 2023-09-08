import unittest
from unittest.mock import Mock
from modules import valid_status
from exceptions import NonRetryableStatusCodeError, FatalStatusCodeError
import requests


class TestValidStatus(unittest.TestCase):

    def test_valid_status_valid_status(self):
        # Create a mock Response object with a valid status code
        response = Mock(spec=requests.Response)
        response.status_code = 200

        # The function should return True for valid statuses
        result = valid_status(response)
        self.assertTrue(result)

    def test_valid_status_retryable_status(self):
        # Create a mock Response object with a retryable status code
        response = Mock(spec=requests.Response)
        response.status_code = 429

        # The function should return False for retryable statuses
        result = valid_status(response)
        self.assertFalse(result)

    def test_valid_status_non_retryable_status(self):
        # Create a mock Response object with a non-retryable status code
        response = Mock(spec=requests.Response)
        response.status_code = 308

        # The function should raise a NonRetryableStatusCodeError
        with self.assertRaises(NonRetryableStatusCodeError) as context:
            valid_status(response)

        # Check that the error message is as expected
        self.assertIn("Cannot retry. Non-retryable status: 308",
                      str(context.exception))

    def test_valid_status_fatal_status(self):
        # Create a mock Response object with a fatal status code
        response = Mock(spec=requests.Response)
        response.status_code = 403

        # The function should raise a FatalStatusCodeError
        with self.assertRaises(FatalStatusCodeError) as context:
            valid_status(response)

        # Check that the error message is as expected
        self.assertIn(
            "Fatal status code: 403. Raspberry request will stop.", str(context.exception))


if __name__ == '__main__':
    unittest.main()
