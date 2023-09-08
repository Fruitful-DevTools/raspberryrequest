import unittest
from unittest.mock import patch
from modules import calculate_backoff


class TestCalculateBackoff(unittest.TestCase):

    @patch('modules.calculate_backoff.random.uniform')
    def test_calculate_backoff(self, mock_uniform):
        # Set the mocked return value for random.uniform
        mock_uniform.side_effect = [0.5, 0.5, 0.5]

        # Test with attempt_number = 0
        result_0 = calculate_backoff(0)
        self.assertEqual(result_0, 1.5)  # Delay = 1 * (1 + 0.5) = 1.5

        # Test with attempt_number = 1
        result_1 = calculate_backoff(1)
        self.assertEqual(result_1, 3.0)  # Delay = 2 * (1 + 0.5) = 3.0

        # Test with attempt_number = 5 (limited to a maximum delay of 10)
        result_5 = calculate_backoff(5)
        # Delay = 10 * (1 + 0.5) = 15.0 (limited to 10)
        self.assertEqual(result_5, 15.0)

        # Verify that random.uniform was called with the correct arguments
        mock_uniform.assert_called_with(0, 1)
        self.assertEqual(mock_uniform.call_count, 3)


if __name__ == '__main__':
    unittest.main()
