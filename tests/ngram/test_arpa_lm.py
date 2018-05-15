import os
import filecmp
import unittest
from ccquery.ngram import ArpaLanguageModel
from ccquery.utils import io_utils

class TestArpaLM(unittest.TestCase):
    """Test the ArpaLanguageModel load and change methods"""

    def setUp(self):
        """Set up local variables"""

        self.arpa = os.path.join(os.path.dirname(__file__), 'sample-model.arpa')
        self.bin = io_utils.change_extension(self.arpa, 'bin')
        self.tmp = io_utils.change_extension(self.arpa, 'tmp.bin')

        io_utils.check_file_readable(self.arpa)
        io_utils.check_file_readable(self.bin)

    def tearDown(self):
        """Remove temporary file"""
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def test_load_model(self):
        """Test loading a n-gram language model from an arpa file"""

        model = ArpaLanguageModel(self.arpa)
        self.assertEqual(model.order, 3)
        self.assertEqual(
            sorted(model.total.items()),
            [(1, 503), (2, 1609), (3, 2162)])

    def test_change_model(self):
        """Test storing a binary marisa-trie based language model"""

        model = ArpaLanguageModel(self.arpa)
        model.save_trie(self.tmp)

        self.assertTrue(
            filecmp.cmp(self.bin, self.tmp, shallow=False),
            'Generated model different from reference model')
