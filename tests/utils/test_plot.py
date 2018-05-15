import os
import unittest
from ccquery.utils import plot_utils

class TestPlot(unittest.TestCase):
    """Test the configuration loader"""

    def setUp(self):
        """Set temporary files"""
        self.tmp_file = os.path.join(os.path.dirname(__file__), 'plot.png')

    def tearDown(self):
        """Delete temporary files"""
        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)

    def test_length(self):
        with self.assertRaises(Exception) as context:
            plot_utils.length_plot('', [], '', '', '')
        self.assertTrue('Method expects a dict' in str(context.exception))

        plot_utils.length_plot(
            self.tmp_file,
            {1:10, 2:5, 3: 4, 7: 8},
            'Bars', 'Keys', 'Values')
        self.assertTrue(os.path.exists(self.tmp_file))

    def test_histogram_1(self):
        with self.assertRaises(Exception) as context:
            plot_utils.occurrences_plot('', {}, [], '', '', '')
        self.assertTrue('Method expects a list' in str(context.exception))

        plot_utils.occurrences_plot(
            self.tmp_file,
            [1, 10, 2, 5, 3, 4, 7, 8],
            [1, 2, 3],
            'Histogram', 'Keys', 'Values')
        self.assertTrue(os.path.exists(self.tmp_file))

    def test_histogram_2(self):
        plot_utils.occurrences_plot(
            self.tmp_file,
            [1, 10, 2, 5, 3, 4, 7, 8],
            [1, 2, 3, 5],
            'Histogram', 'Keys', 'Values',
            left_lim=[0, 10],
            right_lim=[50, 104])
        self.assertTrue(os.path.exists(self.tmp_file))
