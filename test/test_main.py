from unittest.mock import MagicMock
import unittest
from unittest.mock import patch

from main import APIRequestHandler
from exceptions import MaxRetryError, FatalStatusCodeError

import unittest
from unittest.mock import MagicMock

handler = APIRequestHandler({'test': 'test'})


class TestSendApiRequest(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()
        self.headers = {'Content-Type': 'application/json'}
        self.max_retry_attempts = 3
        self.attempt_number = 0
        self.handler = APIRequestHandler({'test': 'test'})

    def tearDown(self):
        self.session = None

    def test_send_api_request_success(self):
        # Testing a successful API request
        base_url = 'https://api.example.com'
        method = 'GET'
        params = {'param1': 'value1', 'param2': 'value2'}
        data = {'key1': 'value1', 'key2': 'value2'}
        headers = {'Authorization': 'Bearer token'}

        # Mocking the make_request function to simulate a successful response
        make_request_mock = MagicMock(
            return_value=MagicMock(json=lambda: {'result': 'success'}))
        with patch('components.make_request', make_request_mock):
            response = handler.send_api_request(
                base_url, method, params, data, headers)

        self.assertEqual(response, {'result': 'success'})

    def test_send_api_request_retry(self):
        # Testing a retry scenario
        base_url = 'https://api.example.com'
        method = 'GET'
        params = {'param1': 'value1', 'param2': 'value2'}
        data = {'key1': 'value1', 'key2': 'value2'}
        headers = {'Authorization': 'Bearer token'}

        # Mocking the make_request function to simulate an unsuccessful response
        make_request_mock = MagicMock(
            return_value=MagicMock(json=lambda: {'result': 'retry'}))
        with patch('components.make_request', make_request_mock):
            response = handler.send_api_request(
                base_url, method, params, data, headers)

        self.assertEqual(response, {'result': 'retry'})

    def test_send_api_request_fatal_status_code(self):
        # Testing a fatal status code scenario
        base_url = 'https://api.example.com'
        method = 'GET'
        params = {'param1': 'value1', 'param2': 'value2'}
        data = {'key1': 'value1', 'key2': 'value2'}
        headers = {'Authorization': 'Bearer token'}

        # Mocking the make_request function to simulate a fatal status code
        make_request_mock = MagicMock(side_effect=FatalStatusCodeError)
        with patch('components.make_request', make_request_mock):
            with self.assertRaises(FatalStatusCodeError):
                handler.send_api_request(
                    base_url, method, params, data, headers)


class TestBackoff(unittest.TestCase):

    def setUp(self) -> None:
        self.handler = APIRequestHandler({'test': 'test'})

    @patch('time.sleep')
    def test_backoff(self, mock_sleep):
        # Testing normal behavior
        self.handler.attempt_number = 1
        self.handler.backoff()
        mock_sleep.assert_called_once()

        # Testing maximum retry attempts
        self.handler.attempt_number = 5
        with self.assertRaises(MaxRetryError):
            self.handler.backoff()


if __name__ == '__main__':
    unittest.main()
