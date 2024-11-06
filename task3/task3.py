import unittest
import numpy as np

def cyclic_time_features(time_str):
    """
    Converts a time string in "HH:MM" format into cyclic time features.

    Args:
      time_str: The time string in "HH:MM" format.

    Returns:
      A tuple of two floats representing the sin and cos components of the cyclic time.
    """
    hour, minute = map(int, time_str.split(':'))
    total_minutes = hour * 60 + minute
    angle = 2 * np.pi * total_minutes / (24 * 60)  # Convert to radians
    return np.sin(angle), np.cos(angle)


class TestCyclicTimeFeatures(unittest.TestCase):

    def test_midnight(self):
        sin_val, cos_val = cyclic_time_features("00:00")
        self.assertAlmostEqual(sin_val, 0.0)
        self.assertAlmostEqual(cos_val, 1.0)

    def test_noon(self):
        sin_val, cos_val = cyclic_time_features("12:00")
        self.assertAlmostEqual(sin_val, 0.0)
        self.assertAlmostEqual(cos_val, -1.0)

    def test_6am(self):
        sin_val, cos_val = cyclic_time_features("06:00")
        self.assertAlmostEqual(sin_val, 1.0)
        self.assertAlmostEqual(cos_val, 0.0)

    def test_6pm(self):
        sin_val, cos_val = cyclic_time_features("18:00")
        self.assertAlmostEqual(sin_val, -1.0)
        self.assertAlmostEqual(cos_val, 0.0)

    def test_time_difference_across_midnight(self):
        """Tests the time difference between 23:00 and 01:00."""
        sin_23, cos_23 = cyclic_time_features("23:00")
        sin_01, cos_01 = cyclic_time_features("01:00")

        # Calculate the angular distance
        angle_diff = np.arccos(sin_23 * sin_01 + cos_23 * cos_01)
        time_diff_hours = (angle_diff / (2 * np.pi)) * 24

        self.assertAlmostEqual(time_diff_hours, 2.0, delta=0.01)  # Allow for small rounding errors


if __name__ == '__main__':
    unittest.main()
