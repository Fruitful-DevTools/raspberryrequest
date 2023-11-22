import unittest
from unittest.mock import patch, call
import requests
from raspberryrequest.main import APIRequestHandler
from raspberryrequest.exceptions import MaxRetryError, NonRetryableStatusCodeError

handler = APIRequestHandler({'test': 'test'})


def make_request_obj(status):
    response = requests.Response()
    response.reason = '{"test": "test", "test2": "test2"}'
    response.status_code = status
    return response


class TestSendApiRequest(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://reqres.in/api/users/2"
        self.method = "GET"
        self.params = {"param1": "value1", "param2": "value2"}
        self.data = {"key1": "value1", "key2": "value2"}
        self.headers = {"Content-Type": "application/json"}
        self.api_client = APIRequestHandler(headers=self.headers)

    def test_happy_path(self):
        validate_return = True
        expected = {
            "data": {
                "id": 2,
                "email": "janet.weaver@reqres.in",
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://reqres.in/img/faces/2-image.jpg"
            },
            "support": {
                "url": "https://reqres.in/#support-heading",
                "text": "To keep ReqRes free, contributions towards server costs are appreciated!"
            }
        }
        with patch("raspberryrequest.main.valid_status") as mock_valid_status:
            mock_valid_status.return_value = validate_return
            response = self.api_client.send_api_request(
                self.base_url, self.method, self.params, self.headers)
        self.assertDictEqual(expected, response)

    def test_timeout_error(self):
        with patch("requests.Session.send") as mock_send:
            mock_send.side_effect = requests.exceptions.Timeout
            with self.assertRaises(MaxRetryError):
                self.api_client.send_api_request(
                    self.base_url, self.method, self.params, self.headers)
            attempts = self.api_client.calls()
            self.assertEqual(attempts, 3)

    def test_HTTPError(self):
        with patch("requests.Session.send") as mock_send:
            mock_send.side_effect = requests.exceptions.HTTPError
            with self.assertRaises(MaxRetryError):
                self.api_client.send_api_request(
                    self.base_url, self.method, self.params, self.headers)
            attempts = self.api_client.calls()
            self.assertEqual(attempts, 3)

    def test_NonRetryableStatusCodeError(self):
        self.base_url = "https://reqres.in/api/users/23"

        result = self.api_client.send_api_request(
            self.base_url, self.method, self.params, self.headers)
        self.assertIsNone(result)

    def test_FatalStatusCodeError(self):
        pass

    def test_edge_case_no_base_url(self):
        pass

    def test_edge_case_none_params(self):
        pass

    def test_edge_case_none_headers(self):
        pass


if __name__ == '__main__':
    unittest.main()
