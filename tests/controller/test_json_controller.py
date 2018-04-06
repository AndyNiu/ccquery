import os
import filecmp
import unittest
from ccquery.data import json_controller
from ccquery.utils import io_utils

class TestJsonController(unittest.TestCase):
    """Test the json controller methods"""

    def setUp(self):
        """Set up local variables"""

        self.jsonl_file = os.path.join(
            os.path.dirname(__file__), 'sample.jsonl')
        self.txt_file = io_utils.change_extension(self.jsonl_file, 'txt')
        self.copy_txt = io_utils.change_extension(self.jsonl_file, 'copy.txt')

        io_utils.check_file_readable(self.jsonl_file)

    def test_load_jsonl(self):
        """Load json-lines data"""

        keys = [
            'baths', 'beds', 'city', 'latitude', 'longitude',
            'price', 'sale_date', 'sq__ft', 'state', 'type', 'zip']

        cities = ['SACRAMENTO'] * 8 + ['RANCHO CORDOVA', 'RIO LINDA']

        data = json_controller.load_fields(self.jsonl_file, keys)

        self.assertEqual(keys, sorted(list(data.keys())))
        self.assertEqual(10, len(data[keys[0]]))
        self.assertEqual(cities, data['city'])

    def test_load_field_jsonl(self):
        """Load json-lines data for one single field"""

        cities = ['SACRAMENTO'] * 8 + ['RANCHO CORDOVA', 'RIO LINDA']
        data = json_controller.load_field(self.jsonl_file, 'city')
        self.assertEqual(cities, data)

    def test_load_chunk(self):
        """Load partial data"""
        input_data, target_data = json_controller.load_chunk(
            self.jsonl_file, 5, input_field='city', target_field='zip')
        self.assertEqual(5, len(input_data))
        self.assertEqual(5, len(target_data))

    def test_stream_jsonl(self):
        """Load one entry at a time"""

        index = 0
        input_data = ['SACRAMENTO'] * 8 + ['RANCHO CORDOVA', 'RIO LINDA']
        target_data = [
            95838, 95823, 95815, 95815, 95824,
            95841, 95842, 95820, 95670, 95673]

        for input_value, target_value in json_controller.stream(
                self.jsonl_file, input_field='city', target_field='zip'):
            self.assertEqual(input_value, input_data[index])
            self.assertEqual(target_value, target_data[index])
            index += 1

    def test_stream_field_jsonl(self):
        """Load one field from one entry at a time"""

        cities = ['SACRAMENTO'] * 8 + ['RANCHO CORDOVA', 'RIO LINDA']
        values = list(json_controller.stream_field(self.jsonl_file, 'city'))
        self.assertEqual(cities, values)

    def test_stream_chunk_jsonl(self):
        """Load partial data"""

        cities = ['SACRAMENTO'] * 5
        zip_codes = [95838, 95823, 95815, 95815, 95824]
        values = json_controller.stream_chunk(self.jsonl_file, 5, 'city', 'zip')
        values = list(values)[0]
        self.assertEqual(cities, values[0])
        self.assertEqual(zip_codes, values[1])

    def test_store_txt(self):
        """Store content to text file"""

        data = json_controller.load_field(self.jsonl_file, 'city')
        json_controller.store_text(data, self.copy_txt)

        self.assertTrue(
            filecmp.cmp(self.copy_txt, self.txt_file, shallow=False),
            'Output file different from input file')

    def tearDown(self):
        """Remove temporary files"""
        if os.path.exists(self.copy_txt):
            os.remove(self.copy_txt)
