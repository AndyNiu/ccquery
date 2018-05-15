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
        io_utils.check_file_readable(self.dic)
        io_utils.check_file_readable(self.samples)

    def test_extra_load(self):
        """Add an extra dictionary"""

        spell_checker = HunSpelling(self.dic, self.aff, self.dic)
        self.assertFalse(None, spell_checker)

    def test_spellings(self):
        """Check spellings"""

        spell_checker = HunSpelling(self.dic, self.aff)
        words = ['aide', 'brut', 'pourquoi', 'calcul', 'ville']
        errors = [spell_checker.is_misspelled(w) for w in words]
        self.assertEqual([False, False, True, False, True], errors)

        # incorrectly test adding new words
        spell_checker.add_words(None)

        # add new words and recheck spelling
        nwords = ['pourquoi', 'ville']
        spell_checker.add_words(nwords)
        errors = [spell_checker.is_misspelled(w) for w in nwords]
        self.assertEqual([False, False], errors)

        # remove the newly added words and recheck spelling
        spell_checker.remove_words(None)
        spell_checker.remove_words(nwords)
        errors = [spell_checker.is_misspelled(w) for w in nwords]
        self.assertEqual([True, True], errors)

    def test_new_dict(self):
        """Test adding an extra dictionary"""

        spell_checker = HunSpelling(self.dic, self.aff)
        spell_checker.add_extra_dictionary(self.dic)
        self.assertFalse(None, spell_checker)

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
