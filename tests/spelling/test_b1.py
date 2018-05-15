import os
import unittest
from ccquery.utils import io_utils
from ccquery.spelling import B1Correction

class TestBaseline1(unittest.TestCase):
    """Test the performance evaluation of automation corrections"""

    def setUp(self):
        """Set up local variables"""

        nlp = 'fr_core_news_sm'
        aff = os.path.join(os.path.dirname(__file__), 'index.aff')
        dic = os.path.join(os.path.dirname(__file__), 'index.dic')

        ngram = os.path.join(
            os.path.dirname(__file__), '..', 'ngram', 'sample-model.bin')

        io_utils.check_file_readable(aff)
        io_utils.check_file_readable(dic)
        io_utils.check_file_readable(ngram)

        # load baseline
        self.model = B1Correction()
        self.model.load_spacy(nlp, disable=['ner', 'parser'])
        self.model.load_hunspell(dic, aff)
        self.model.load_ngram(ngram)

    def tearDown(self):
        """Remove temporary file"""
        if self.model:
            del self.model

    def test_baseline(self):
        """Test corrections made by test-baseline"""

        queries = [
            'comment rehoindre une force',
            'meilleur voeu en portugais',
            'serrue en applique',
            'pain de mie japonaid',
            'dance polynesienne',
        ]

        refs = [
            'comme histoire une forme',
            'meillet eux en important',
            'utiliser en pratique',
            'ainsi de emil application',
            'france polynômes',
        ]

        solutions = []
        for query in queries:
            candidates = self.model.correct(query, topn=1)
            solutions.append(candidates[0])

        self.assertEqual(refs, solutions)
