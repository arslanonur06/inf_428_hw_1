import unittest
import random

def generate_random_data(mean, variance, sample_size):
    """Generates a list of random threat scores with a given mean, variance, and sample size."""
    return [min(90, max(0, int(random.gauss(mean, variance)))) for _ in range(sample_size)]

def calculate_aggregated_threat_score(department_data, importance_weights):
    """
    Calculates the aggregated user cybersecurity threat score.

    Args:
      department_data: A dictionary where keys are department names and values are lists of user threat scores.
      importance_weights: A dictionary where keys are department names and values are importance weights (1-5).

    Returns:
      The aggregated threat score (0-90).
    """

    weighted_scores = []
    for dept, scores in department_data.items():
        mean_score = sum(scores) / len(scores) if scores else 0
        weighted_score = mean_score * importance_weights[dept]
        weighted_scores.append(weighted_score)

    # Normalize to 0-90 range
    max_possible_score = 90 * sum(importance_weights.values())
    aggregated_score = (sum(weighted_scores) / max_possible_score) * 90

    return round(aggregated_score, 2)


class TestAggregatedThreatScore(unittest.TestCase):

    def test_no_threat(self):
        """All departments have no threat."""
        department_data = {
            "Engineering": [0] * 50,
            "Marketing": [0] * 30,
            "Finance": [0] * 20,
            "HR": [0] * 15,
            "Science": [0] * 100,
        }
        importance_weights = {
            "Engineering": 1,
            "Marketing": 1,
            "Finance": 1,
            "HR": 1,
            "Science": 1,
        }
        self.assertEqual(calculate_aggregated_threat_score(department_data, importance_weights), 0)

    def test_uniform_threat(self):
        """All departments have a uniform, moderate threat level."""
        department_data = {
            "Engineering": [45] * 50,
            "Marketing": [45] * 30,
            "Finance": [45] * 20,
            "HR": [45] * 15,
            "Science": [45] * 100,
        }
        importance_weights = {
            "Engineering": 1,
            "Marketing": 1,
            "Finance": 1,
            "HR": 1,
            "Science": 1,
        }
        self.assertEqual(calculate_aggregated_threat_score(department_data, importance_weights), 45)

    def test_varying_threat_levels(self):
        """Departments have different average threat levels."""
        department_data = {
            "Engineering": [60] * 50,
            "Marketing": [30] * 30,
            "Finance": [75] * 20,
            "HR": [15] * 15,
            "Science": [45] * 100,
        }
        importance_weights = {
            "Engineering": 1,
            "Marketing": 1,
            "Finance": 1,
            "HR": 1,
            "Science": 1,
        }
        # Expect the aggregated score to be close to the average of the department averages
        expected_score = (60 + 30 + 75 + 15 + 45) / 5
        self.assertAlmostEqual(calculate_aggregated_threat_score(department_data, importance_weights), expected_score, delta=1)

    def test_varying_importance(self):
        """Departments have different importance levels."""
        department_data = {
            "Engineering": [60] * 50,
            "Marketing": [30] * 30,
            "Finance": [75] * 20,
            "HR": [15] * 15,
            "Science": [45] * 100,
        }
        importance_weights = {
            "Engineering": 5,
            "Marketing": 2,
            "Finance": 4,
            "HR": 1,
            "Science": 3,
        }
        # Expect a higher score due to the higher importance of Engineering and Finance
        self.assertGreater(calculate_aggregated_threat_score(department_data, importance_weights), 45)

    def test_outliers(self):
        """Some departments have outliers with very high threat scores."""
        department_data = {
            "Engineering": [60] * 50 + [90] * 5,  # 10% outliers
            "Marketing": [30] * 30,
            "Finance": [75] * 20,
            "HR": [15] * 15,
            "Science": [45] * 100,
        }
        importance_weights = {
            "Engineering": 1,
            "Marketing": 1,
            "Finance": 1,
            "HR": 1,
            "Science": 1,
        }
        # Expect a slightly higher score due to the outliers in Engineering
        self.assertGreater(calculate_aggregated_threat_score(department_data, importance_weights), 45)

    def test_functional_case_1(self):
        """
        Functional test case 1:
        - Each department has no outliers.
        - Each department mean threat score are NOT far from each other.
        - Similar number of users.
        - All departments have the same importance.
        """
        department_data = {
            "Engineering": generate_random_data(mean=40, variance=5, sample_size=50),
            "Marketing": generate_random_data(mean=45, variance=5, sample_size=40),
            "Finance": generate_random_data(mean=50, variance=5, sample_size=45),
            "HR": generate_random_data(mean=42, variance=5, sample_size=55),
            "Science": generate_random_data(mean=48, variance=5, sample_size=50),
        }
        importance_weights = {
            "Engineering": 1,
            "Marketing": 1,
            "Finance": 1,
            "HR": 1,
            "Science": 1,
        }
        # Expect the score to be close to the average of the means
        expected_score = (40 + 45 + 50 + 42 + 48) / 5
        self.assertAlmostEqual(calculate_aggregated_threat_score(department_data, importance_weights), expected_score, delta=3)


if __name__ == '__main__':
    unittest.main()
