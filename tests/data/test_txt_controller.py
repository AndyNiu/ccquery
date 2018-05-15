import os
import unittest
from ccquery.data import text_controller
from ccquery.utils import io_utils

class TestTextController(unittest.TestCase):
    """Test the text controller methods"""

    def setUp(self):
        """Set up local variables"""
        self.txt_file = os.path.join(os.path.dirname(__file__), 'sample.txt')
        io_utils.check_file_readable(self.txt_file)

    def test_load_text(self):
        """Load text data"""

        cities = ['SACRAMENTO'] * 8 + ['RANCHO CORDOVA', 'RIO LINDA']
        data = text_controller.load(self.txt_file)
        self.assertEqual(cities, data)

    def test_load_chunk_text(self):
        """Load partial text data"""

        # without shuffle
        cities = ['SACRAMENTO'] * 5
        data = text_controller.load_chunk(self.txt_file, 5)
        self.assertEqual(cities, data)

        # with shuffle
        data = text_controller.load_chunk(self.txt_file, 5, to_shuffle=True)
        self.assertEqual(5, len(data))

    def test_stream_text(self):
        """Stream text data"""

        cities = ['SACRAMENTO'] * 8 + ['RANCHO CORDOVA', 'RIO LINDA']
        data = list(text_controller.stream(self.txt_file))
        self.assertEqual(cities, data)

    def test_stream_chunk_text(self):
        """Stream partial text data"""

        cities = ['SACRAMENTO'] * 5
        data = text_controller.stream_chunk(self.txt_file, n=5)
        self.assertEqual(cities, list(data)[0])
