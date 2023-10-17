import unittest
import pytest
from raspberryrequest.modules import make_request
from unittest.mock import Mock, patch


class MakeRequestTestCase(unittest.TestCase):
    @patch('raspberryrequest.modules.make_request.requests.Session')
    def test_make_request_get(self, mock_session):
        # Create a mock response object for the request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Success"}

        # Create a mock session instance and configure it to return the mock response
        mock_get = Mock(return_value=mock_response)
        mock_session.return_value.get = mock_get

        base_url = "http://example.com"
        method = "GET"
        headers = {"Content-Type": "application/json"}
        params = {"param1": "value1"}
        data = {}

        # Call your make_request function with the mock session
        response = make_request(
            base_url, method, headers, params, data, mock_session())

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success"})
        mock_get.assert_called_once_with(
            base_url, headers=headers, params=params)

    @patch('raspberryrequest.modules.make_request.requests.Session')
    def test_make_request_post(self, mock_session):
        # Create a mock response object for the request
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"message": "Created"}

        # Create a mock session instance and configure it to return the mock response
        mock_post = Mock(return_value=mock_response)
        mock_session.return_value.post = mock_post

        base_url = "http://example.com"
        method = "POST"
        headers = {"Content-Type": "application/json"}
        params = {}
        data = {"key": "value"}

        # Call your make_request function with the mock session
        response = make_request(
            base_url, method, headers, params, data, mock_session())

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Created"})
        mock_post.assert_called_once_with(
            base_url, headers=headers, params=params, json=data)

    @patch('raspberryrequest.modules.make_request.requests.Session')
    def test_make_request_invalid_method(self, mock_session):
        base_url = "http://example.com"
        method = "PUT"  # An invalid HTTP method
        headers = {"Content-Type": "application/json"}
        params = {}
        data = {}
        session = mock_session()

        with pytest.raises(ValueError):
            make_request(base_url, method, headers, params, data, session)


if __name__ == "__main__":
    unittest.main()
