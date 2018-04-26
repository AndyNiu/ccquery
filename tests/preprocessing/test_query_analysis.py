import os
import json
import unittest
from ccquery.utils import io_utils
from ccquery.preprocessing import QueryAnalysis

class TestQuery(unittest.TestCase):
    """Test the mix of two hunspell dictionaries"""

    def setUp(self):
        """Set up local variables"""

        self.jsonl = os.path.join(
            os.path.dirname(__file__), '..', 'spelling', 'sample-queries.jsonl')
        self.csv = os.path.join(os.path.dirname(__file__), 'temp.csv')
        self.txt = os.path.join(os.path.dirname(__file__), 'temp.txt')

        self.temp_png = os.path.join(os.path.dirname(__file__), 'temp.png')
        self.temp_json = os.path.join(os.path.dirname(__file__), 'temp.json')

        data = []
        with open(self.jsonl, 'r', encoding='utf-8') as istream:
            for line in istream:
                data.append(json.loads(line))

        # store under csv format
        with open(self.csv, 'w', encoding='utf-8') as ostream:
            ostream.write(','.join(data[0].keys()) + '\n')
            for query in data:
                ostream.write(
                    ','.join(['"' + q + '"' for q in query.values()]) + '\n')

        # store under txt format
        with open(self.txt, 'w', encoding='utf-8') as ostream:
            for query in data:
                ostream.write("{}\n".format(query['noisy']))

    def tearDown(self):
        """Delete temporary files"""
        io_utils.delete_file(self.csv)
        io_utils.delete_file(self.txt)
        io_utils.delete_file(self.temp_png)
        io_utils.delete_file(self.temp_json)

    def test_bad_token(self):
        """Test wrong token"""

        with self.assertRaises(Exception) as context:
            QueryAnalysis(self.jsonl, token='token', field='noisy')
        self.assertTrue('Unknown token type' in str(context.exception))

    def test_bad_extension(self):
        """Test wrong file extension"""

        fn = io_utils.change_extension(self.jsonl, 'png')
        with self.assertRaises(Exception) as context:
            QueryAnalysis(fn, token='word', field='noisy')
        self.assertTrue('Unknown file extension' in str(context.exception))

    def test_load_jsonl(self):
        """Test loading queries from jsonl file"""

        analysis = QueryAnalysis(self.jsonl, token='word', field='noisy')
        analysis.analyze_text()
        self.assertEqual(300, analysis.nqueries)

    def test_load_csv(self):
        """Test loading queries from csv file"""

        analysis = QueryAnalysis(
            self.csv, token='word', field='noisy', header=0)
        analysis.analyze_text()
        self.assertEqual(300, analysis.nqueries)

    def test_load_text(self):
        """Test loading queries from text file"""

        analysis = QueryAnalysis(self.txt, token='word')
        analysis.analyze_text()
        self.assertEqual(300, analysis.nqueries)

    def test_words(self):
        """Test word analysis"""

        analysis = QueryAnalysis(self.jsonl, token='word', field='noisy')
        analysis.analyze_text(cleaner='get_words')

        analysis.plot_query_length(self.temp_png)
        self.assertTrue(os.path.exists(self.temp_png))

        analysis.info_tokens()
        self.assertEqual(816, len(analysis.data))

    def test_chars(self):
        """Test char analysis"""

        analysis = QueryAnalysis(self.jsonl, token='char', field='noisy')
        analysis.analyze_text(cleaner='get_characters')

        analysis.plot_minoccurrences(self.temp_png, mins=[1, 2, 3])
        self.assertTrue(os.path.exists(self.temp_png))

        analysis.info_tokens()
        self.assertEqual(51, len(analysis.data))

        tokens = {
            "'": 20, ',': 1, '.': 2, '0': 7, '1': 6, '2': 6, '3': 2, '4': 2,
            '6': 1, '7': 2, '8': 1, '9': 1, '?': 2, 'a': 570, 'b': 93, 'c': 288,
            'd': 214, 'e': 1015, 'f': 87, 'g': 143, 'h': 110, 'i': 493, 'j': 19,
            'k': 20, 'l': 338, 'm': 254, 'n': 501, 'o': 456, 'p': 220, 'q': 35,
            'r': 551, 's': 457, 't': 448, 'u': 338, 'v': 92, 'w': 6, 'x': 36,
            'y': 25, 'z': 5, 'à': 10, 'â': 5, 'ç': 3, 'è': 10, 'é': 94, 'ê': 8,
            'ë': 1, 'î': 3, 'ï': 1, 'ô': 6, 'œ': 4, '’': 1
        }
        self.assertEqual(tokens, dict(analysis.data))

        analysis.save_tokens(self.temp_json)
        self.assertTrue(os.path.exists(self.temp_json))
