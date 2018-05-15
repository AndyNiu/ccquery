import os
import unittest
from ccquery.spelling import Evaluation
from ccquery.utils import io_utils

class TestEvalSpelling(unittest.TestCase):
    """Test the performance evaluation of automation corrections"""

    def setUp(self):
        """Set up local variables"""
        self.cfile = os.path.join(
            os.path.dirname(__file__), 'sample-queries.jsonl')

    def test_do_nothing(self):
        """Test the performance of a 'do nothing' algorithm"""

        evaluation = Evaluation()

        for n in [10, 5, 1]:
            evaluation.load_from_file(self.cfile, 'noisy', 'clean')
            scores = evaluation.performance(n)
            self.assertEqual(scores, (83.33, 83.33, 83.33))

    def test_perfect_correction(self):
        """Test the performance of a 'perfect correction' algorithm"""

        evaluation = Evaluation()
        evaluation.load_from_file(self.cfile, 'clean', 'clean')

        scores = evaluation.performance(1)
        self.assertEqual(scores, (100.00, 100.00, 100.00))

    def test_empty_data(self):
        """Test the performance on an empty data"""

        evaluation = Evaluation()
        evaluation.load_from_list([])

        with self.assertRaises(Exception) as context:
            evaluation.performance(1)
        self.assertTrue('No corrections available' in str(context.exception))
