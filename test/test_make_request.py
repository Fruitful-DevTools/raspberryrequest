import unittest
import requests
from raspberryrequest.request import make_request
from unittest.mock import Mock, patch, call


class MakeRequestTestCase(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.send_path = 'raspberryrequest.request.requests.Session.send'
        self.prepare_request_path = 'raspberryrequest.request.requests.Session.prepare_request'
        self.response_obj = requests.Response()
        self.response_obj.headers['Content-Type'] = 'application/json'

        self.request_obj = requests.Request(
            method="GET", url="http://example.com", headers={}, params={})
        self.prepared_request_obj = self.session.prepare_request(
            self.request_obj)

    def test_make_request_get(self):
        # Create a mock response object for the request
        self.response_obj.status_code = 200
        response_message = '{"message": "Success"}'
        self.response_obj._content = response_message.encode('utf-8')

        base_url = "http://example.com"
        method = "GET"
        headers = {"Content-Type": "application/json"}
        params = {"param1": "value1"}

        with patch(self.send_path) as mock_send:
            mock_send.return_value = self.response_obj
            # Call your make_request function with the mock session
            response = make_request(
                base_url, method, headers, params, self.session)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success"})


if __name__ == "__main__":
    unittest.main()
