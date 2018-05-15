import os
import json
import filecmp
import unittest
from ccquery.utils import io_utils
from ccquery.preprocessing import Vocabulary

class TestVocab(unittest.TestCase):
    """Test the vocabulary"""

    def setUp(self):
        """Set up local variables"""

        self.corpus = os.path.join(
            os.path.dirname(__file__), 'sample-corpus.txt')
        self.vocab = os.path.join(
            os.path.dirname(__file__), 'sample-vocab.txt')

        self.files = {
            'tvoc': os.path.join(os.path.dirname(__file__), 'vocab.txt'),
            'jvoc': os.path.join(os.path.dirname(__file__), 'vocab.json'),
            'plot': os.path.join(os.path.dirname(__file__), 'vocab.png'),
        }

    def tearDown(self):
        """Delete temporary files"""
        for file in self.files.values():
            io_utils.delete_file(file)

    def test_word_vocabulary_1(self):
        """Test creating, filtering, plotting and saving a word vocabulary"""

        # test bad load
        with self.assertRaises(Exception) as context:
            vocab = Vocabulary(path={}, token='word')
        self.assertTrue('file path or a dictionary' in str(context.exception))

        with self.assertRaises(Exception) as context:
            vocab = Vocabulary(path={}, token='token')
        self.assertTrue("'word' or a 'char' token" in str(context.exception))

        # test good load
        vocab = Vocabulary(path=self.corpus, token='word')

        vocab.plot_minoccurrences(self.files['plot'], mins=[1, 2, 3])
        self.assertTrue(os.path.exists(self.files['plot']))

        # test bad filter
        with self.assertRaises(Exception) as context:
            vocab.filter_tokens()
        self.assertTrue("Method expects either" in str(context.exception))

        # test good filter
        vocab.filter_tokens(topn=500)
        vocab.save_tokens(self.files['tvoc'])

        self.assertTrue(
            filecmp.cmp(self.vocab, self.files['tvoc'], shallow=False),
            'Generated vocabulary different from reference vocabulary')

    def test_word_vocabulary_2(self):
        """Test loading a word vocabulary from counts"""

        counts = {'a': 100, 'b': 123, 'c': 23, 'd': 43}
        vocab = Vocabulary(counts=counts, token='word')
        self.assertEqual(counts, vocab.tokens)
        self.assertEqual(289, vocab.occurrences)

        # test good filter
        vocab.filter_tokens(minocc=50)
        self.assertEqual({'a': 100, 'b': 123}, vocab.tokens)
        self.assertEqual(223, vocab.occurrences)

        # test json save
        vocab.save_tokens(self.files['jvoc'])
        self.assertTrue(os.path.exists(self.files['jvoc']))

        counts = {}
        with open(self.files['jvoc'], 'r') as istream:
            counts = json.load(istream)
        self.assertEqual(counts, vocab.tokens)
