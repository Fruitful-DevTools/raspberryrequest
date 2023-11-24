import unittest
from raspberryrequest.validate import validate_status, update_session_data
from raspberryrequest.exceptions import NonRetryableStatusCodeError, FatalStatusCodeError
from raspberryrequest.models import SessionData, StatusCodes


class TestValidStatus(unittest.TestCase):

    def test_valid_status_valid_status(self):
        code = 200
        status_codes = StatusCodes()
        result = validate_status(
            code, status_codes)
        self.assertTrue(result)

    def test_valid_status_retryable_status(self):
        code = 429
        status_codes = StatusCodes()

        result = validate_status(
            code, status_codes)
        self.assertFalse(result)

    def test_valid_status_non_retryable_status(self):
        code = 308
        status_codes = StatusCodes()

        with self.assertRaises(NonRetryableStatusCodeError) as context:
            validate_status(code, status_codes)

        self.assertIn("Cannot retry. Non-retryable status: 308",
                      str(context.exception))

    def test_valid_status_fatal_status(self):
        code = 403
        status_codes = StatusCodes()

        with self.assertRaises(FatalStatusCodeError) as context:
            validate_status(code, status_codes)

        self.assertIn(
            "Fatal status code: 403. Raspberry request will stop.", str(context.exception))


class TestUpdateSessionData(unittest.TestCase):

    def test_happy_path_paid(self):
        status_code = 200
        session_data = SessionData()
        status_codes = StatusCodes()
        status_codes.PAID.append(200)
        session_data = update_session_data(
            status_code, status_codes, session_data)
        session_data.update_total()
        paid = session_data.PAID
        total = session_data.TOTAL
        self.assertEqual(paid, 1)
        self.assertEqual(total, 1)

    def test_happy_path_unpaid(self):
        status_code = 200
        session_data = SessionData()
        status_codes = StatusCodes()
        status_codes.PAID.remove(200)
        session_data = update_session_data(
            status_code, status_codes, session_data)
        session_data.update_total()
        unpaid = session_data.UNPAID
        total = session_data.TOTAL
        self.assertEqual(unpaid, 1)
        self.assertEqual(total, 1)

    def test_happy_path_valid(self):
        status_code = 200
        session_data = SessionData()
        status_codes = StatusCodes()
        session_data = update_session_data(
            status_code, status_codes, session_data)
        session_data.update_total()

    def test_happy_path_retryable(self):
        status_code = 408
        session_data = SessionData()
        status_codes = StatusCodes()
        session_data = update_session_data(
            status_code, status_codes, session_data)
        session_data.update_total()
        retryable = session_data.RETRYABLE
        total = session_data.TOTAL
        self.assertEqual(retryable, 1)
        self.assertEqual(total, 1)

    def test_happy_path_nonretryable(self):
        status_code = 308
        session_data = SessionData()
        status_codes = StatusCodes()
        session_data = update_session_data(
            status_code, status_codes, session_data)
        session_data.update_total()
        nonretryable = session_data.NONRETRYABLE
        total = session_data.TOTAL
        self.assertEqual(nonretryable, 1)
        self.assertEqual(total, 1)

    def test_happy_path_fatal(self):
        status_code = 403
        session_data = SessionData()
        status_codes = StatusCodes()
        session_data = update_session_data(
            status_code, status_codes, session_data)
        session_data.update_total()
        fatal = session_data.FATAL
        total = session_data.TOTAL
        self.assertEqual(fatal, 1)
        self.assertEqual(total, 1)


if __name__ == '__main__':
    unittest.main()
