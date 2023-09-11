import unittest
from unittest.mock import patch

from main import APIRequestHandler
from exceptions import MaxRetryError

handler = APIRequestHandler({'test': 'test'})


class TestSendApiRequest(unittest.TestCase):

    def setUp(self):
        self.api_client = APIRequestHandler()
        self.base_url = "https://reqres.in/api/"
        self.method = "POST"
        self.params = {"param1": "value1", "param2": "value2"}
        self.data = {"key1": "value1", "key2": "value2"}
        self.headers = {"Content-Type": "application/json"}

    @patch('requests.get')
    def test_send_api_request_success(self, mock_get):
        response_data = {"data": {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg"
        },
            "support": {
            "url": "https://reqres.in/#support-heading",
            "text": "To keep ReqRes free, contributions towards server costs are appreciated!"
        }}
        mock_get.return_value.json.return_value = response_data
        response = self.api_client.send_api_request(
            f'{self.base_url}users/2', method='GET', params=self.params, headers=self.headers)
        self.assertEqual(response, response_data)


if __name__ == '__main__':
    unittest.main()


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
