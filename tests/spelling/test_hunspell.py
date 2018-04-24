import os
import unittest
from ccquery.spelling import HunSpelling
from ccquery.spelling import Evaluation
from ccquery.utils import io_utils, str_utils
from ccquery.data import json_controller

class TestHunSpelling(unittest.TestCase):
    """Test the generation of automation corrections"""

    def setUp(self):
        """Set up local variables"""

        self.dic = os.path.join(os.path.dirname(__file__), 'index.dic')
        self.aff = os.path.join(os.path.dirname(__file__), 'index.aff')
        self.samples = os.path.join(
            os.path.dirname(__file__), 'sample-queries.jsonl')

        io_utils.check_file_readable(self.aff)
        io_utils.check_file_readable(self.samples)

        # prepare index.dic
        # use the wiki test dictionary and add the header linecount
        wiki_dict = os.path.join(
            os.path.dirname(__file__), '..', 'wiki', 'sample-vocab.txt')

        n = io_utils.count_lines(wiki_dict)
        with open(self.dic, 'w', encoding='utf-8') as ostream:
            ostream.write(str(n) + '\n')
            with open(wiki_dict, 'r', encoding='utf-8') as istream:
                for line in istream:
                    ostream.write(line.strip() + '\n')

    def tearDown(self):
        """Remove temporary file"""
        if os.path.exists(self.dic):
            os.remove(self.dic)

    def test_suggestions(self):
        """Test the automatic spelling corrections"""

        spell_checker = HunSpelling(self.dic, self.aff)

        # top 1 candidates
        for query in json_controller.stream_field(self.samples, 'noisy'):
            candidates = spell_checker.correct(query, topn=1)
            self.assertTrue(len(candidates) <= 1)

        # top 5 candidates
        for query in json_controller.stream_field(self.samples, 'noisy'):
            candidates = spell_checker.correct(query, topn=5)
            self.assertTrue(len(candidates) <= 5)

    def test_eval_suggestions(self):
        """Test the evaluation of automatic spelling corrections"""

        spell_checker = HunSpelling(self.dic, self.aff)

        gold_solutions = []
        cand_solutions = []

        # top 1 candidates
        for query, correction in json_controller.stream(
                self.samples, 'noisy', 'clean'):
            candidates = spell_checker.correct(query, topn=1)
            gold_solutions.append(correction)
            cand_solutions.append(candidates)

        evaluation = Evaluation()
        evaluation.load_from_lists(cand_solutions, gold_solutions)
        scores = evaluation.performance(1)

        # 1 / 300 correct suggestions ('méthode de recherche en histoire')
        self.assertEqual(scores, (0.33, 0.33, 0.33))
