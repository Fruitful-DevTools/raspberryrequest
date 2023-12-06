import unittest
from unittest.mock import patch, call
import requests
from raspberryrequest.main import APIRequestHandler
from raspberryrequest.exceptions import MaxRetryError, FatalStatusCodeError

handler = APIRequestHandler({'test': 'test'})


def make_request_obj(status):
    response = requests.Response()
    response.reason = '{"test": "test", "test2": "test2"}'
    response.status_code = status
    return response


class TestSendApiRequest(unittest.TestCase):

    def test_happy_path(self):
        base_url = "https://reqres.in/api/users/2"
        method = "GET"
        params = {"param1": "value1", "param2": "value2"}
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
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
        with patch("raspberryrequest.main.validate_status") as mock_validate_status:
            mock_validate_status.return_value = validate_return
            response = handler.send_api_request(
                base_url, method, params, headers)
        self.assertDictEqual(expected, response)

    def test_timeout_error(self):
        base_url = "https://reqres.in/api/users/2"
        method = "GET"
        params = {"param1": "value1", "param2": "value2"}
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        with patch("requests.Session.send") as mock_send:
            mock_send.side_effect = requests.exceptions.Timeout
            with self.assertRaises(MaxRetryError):
                handler.send_api_request(
                    base_url, method, params, headers)
            attempts = handler.calls
            self.assertEqual(attempts, 3)

    def test_HTTPError(self):
        base_url = "https://reqres.in/api/users/2"
        method = "GET"
        params = {"param1": "value1", "param2": "value2"}
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        with patch("requests.Session.send") as mock_send:
            mock_send.side_effect = requests.exceptions.HTTPError
            with self.assertRaises(MaxRetryError):
                handler.send_api_request(
                    base_url, method, params, headers)
            attempts = handler.calls
            self.assertEqual(attempts, 3)

    def test_NonRetryableStatusCodeError(self):
        base_url = "https://reqres.in/api/users/23"
        method = "GET"
        params = {"param1": "value1", "param2": "value2"}
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        result = handler.send_api_request(
            base_url, method, params, headers)
        self.assertIsNone(result)

    def test_FatalStatusCodeError(self):
        base_url = "https://reqres.in/api/users/2"
        method = "GET"
        params = {"param1": "value1", "param2": "value2"}
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        response = requests.Response()
        response.status_code = 403
        response.reason = "test"
        with patch("requests.Session.send") as mock_send:
            mock_send.return_value = response
            with self.assertRaises(FatalStatusCodeError):
                handler.send_api_request(
                    base_url, method, params, headers)

    def test_close_session(self):
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        handler.session_data.VALID = 1
        handler.close_session()

        valid = handler.session_data.VALID
        retryable = handler.session_data.RETRYABLE
        nonretryable = handler.session_data.NONRETRYABLE
        fatal = handler.session_data.FATAL
        paid = handler.session_data.PAID
        unpaid = handler.session_data.UNPAID
        self.assertEqual(valid, 0)
        self.assertEqual(retryable, 0)
        self.assertEqual(nonretryable, 0)
        self.assertEqual(fatal, 0)
        self.assertEqual(paid, 0)
        self.assertEqual(unpaid, 0)

    def test_add_status_code(self):
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        new_status_code = 260
        expected_list = [200, 201, 260]
        handler.add_status_code("VALID", new_status_code)
        list = handler.status_codes.VALID

        self.assertListEqual(expected_list, list)

    def test_remove_status_code(self):
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        removed_status_code = 260
        expected_list = [200, 201]
        handler.remove_status_code("VALID", removed_status_code)
        list = handler.status_codes.VALID

        self.assertListEqual(expected_list, list)

    def test_get_status_codes(self):
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        status_codes = handler.get_status_codes()
        self.assertEqual(status_codes, handler.status_codes)

    def test_print_status_codes(self):
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        handler.print_status_codes()

    def test_get_session_data(self):
        headers = {"Content-Type": "application/json"}
        handler = APIRequestHandler(headers=headers)
        session_data = handler.get_session_data()
        print("SESSION DATA: ", session_data)
        self.assertIsInstance(session_data, dict)
        print("GET SESSION DATA ONE: ", session_data['PAID'])


class TestGetSessionData(unittest.TestCase):

    def test_happy_path(self):
        paid_status_codes = [200, 201, 404]
        handler = APIRequestHandler(paid_status_codes=paid_status_codes)
        response = make_request_obj(200)
        response._content = b'{"test": "test", "test2": "test2"}'
        with patch("raspberryrequest.request.requests.Session.send") as mock_send:
            mock_send.return_value = response
            handler.send_api_request("https://reqres.in/api/users/2", "GET")
            session_data = handler.get_session_data()
            self.assertEqual(session_data['PAID'], 1)


if __name__ == '__main__':
    unittest.main()
