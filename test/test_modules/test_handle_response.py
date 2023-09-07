from requests import HTTPError
import unittest
from unittest.mock import MagicMock
from modules import handle_response


class HandleResponseTestCase(unittest.TestCase):
    def test_valid_status_code(self):
        response = MagicMock()
        response.status_code = 200
        self.assertTrue(handle_response(response))

    def test_invalid_status_code(self):
        response = MagicMock()
        response.status_code = 404
        with self.assertRaises(HTTPError):
            handle_response(response)

    def test_non_retryable_status_code(self):
        response = MagicMock()
        response.status_code = 500
        self.assertFalse(handle_response(response))


if __name__ == '__main__':
    unittest.main()
