import random
import unittest
from modules import calculate_backoff


class TestCalculateBackoff(unittest.TestCase):
    def test_attempt_number_0(self):
        self.assertEqual(calculate_backoff(0), 0.0)

    def test_attempt_number_1(self):
        backoff = calculate_backoff(1)
        self.assertTrue(0.0 <= backoff <= 2.0)

    def test_attempt_number_5(self):
        backoff = calculate_backoff(5)
        self.assertTrue(0.0 <= backoff <= 32.0)

    def test_attempt_number_10(self):
        self.assertEqual(calculate_backoff(10), 10.0)


if __name__ == '__main__':
    unittest.main()
