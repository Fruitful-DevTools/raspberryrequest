import logging
import requests
import unittest
from unittest.mock import Mock
from modules import handle_error
from exceptions import UnusableStatusCode, FatalStatusCode


class TestHandleError(unittest.TestCase):

    def test_non_retryable_status(self):
        response = Mock(status_code=400)
        handle_error(response)
        logging_info_calls = logging.info.call_args_list
        self.assertIn('Non-retryable status:400', str(logging_info_calls))
        self.assertRaises(UnusableStatusCode, handle_error, response)

    def test_fatal_status(self):
        response = Mock(status_code=500)
        handle_error(response)
        logging_critical_calls = logging.critical.call_args_list
        self.assertIn('Fatal status code received.',
                      str(logging_critical_calls))
        self.assertRaises(FatalStatusCode, handle_error, response)

    def test_attribute_error(self):
        response = Mock(status_code=200)
        handle_error(response)
        self.assertFalse(logging.info.called)
        self.assertFalse(logging.critical.called)


if __name__ == '__main__':
    unittest.main()
