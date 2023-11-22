import unittest
import pytest
import requests
from raspberryrequest.modules import make_request
from unittest.mock import Mock, patch, call


class MakeRequestTestCase(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.send_path = 'raspberryrequest.modules.request.Session.send'
        self.prepare_request_path = 'raspberryrequest.modules.request.Session.prepare_request'
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

        # Create a mock session instance and configure it to return the mock response
        mock_get = Mock(return_value=self.response_obj)

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


"""
    def test_make_request_post(self):
        # Create a mock response object for the request
        mock_response = requests.Response()
        mock_response.status_code = 201
        mock_response.json.return_value = {"message": "Created"}

        # Create a mock session instance and configure it to return the mock response

        base_url = "http://example.com"
        method = "POST"
        headers = {"Content-Type": "application/json"}
        params = {}
        data = {"key": "value"}
        with patch(self.session_path) as mock_session:
            # Call your make_request function with the mock session
            response = make_request(
                base_url, method, headers, params, data, mock_session())

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Created"})
        mock_post.assert_called_once_with(
            base_url, headers=headers, params=params, json=data)

    def test_make_request_invalid_method(self):
        base_url = "http://example.com"
        method = "PUT"  # An invalid HTTP method
        headers = {"Content-Type": "application/json"}
        params = {}
        data = {}
        session = mock_session()

        with pytest.raises(ValueError):
            make_request(base_url, method, headers, params, data, session)"""


if __name__ == "__main__":
    unittest.main()
