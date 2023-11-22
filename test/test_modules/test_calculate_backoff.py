import unittest
import random
from unittest.mock import patch
from raspberryrequest.modules import calculate_backoff


class TestCalculateBackoff(unittest.TestCase):
    def test_happy_path(self):
        test_cases = [1, 2, 3, 4, 5]

        for case in test_cases:
            with self.subTest(f"Happy Path: {case}"):
                expected = 2**case
                if expected > 10:
                    expected = 10

                jitter = random.uniform(0, 1)
                expected = expected * (1 + jitter)
                with patch('random.uniform', return_value=jitter):
                    self.assertEqual(calculate_backoff(case), expected)

    def test_edge_case_zero(self):
        jitter = random.uniform(0, 1)
        expected = (1 + jitter)
        with patch('random.uniform', return_value=jitter):
            self.assertEqual(calculate_backoff(0), expected)

    def test_edge_case_high(self):
        attempt_num = 100
        delay = min(2 ** attempt_num, 10)
        jitter = random.uniform(0, 1)
        expected = delay * (1 + jitter)
        with patch('random.uniform', return_value=jitter):
            self.assertEqual(calculate_backoff(attempt_num), expected)

    def test_raises_no_input(self):
        with self.assertRaises(TypeError):
            calculate_backoff()

    def test_raises_none_input(self):
        with self.assertRaises(TypeError):
            calculate_backoff(None)

    def test_raises_invalid_input(self):
        with self.assertRaises(TypeError):
            calculate_backoff('invalid')


if __name__ == '__main__':
    unittest.main()
