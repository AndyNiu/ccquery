import os
import unittest
from ccquery.utils import cfg_utils

class TestConfig(unittest.TestCase):
    """Test the configuration loader"""

    def setUp(self):
        """Set up local variables"""

        self.cfg_file = os.path.join(
            os.path.dirname(__file__),
            '..', '..', 'conf', 'model', 'config_baseline_1.yml')

        self.empty_file = os.path.join(os.path.dirname(__file__), '__init__.py')
        self.test_file = os.path.join(os.path.dirname(__file__), 'empty.yml')

    def tearDown(self):
        """Delete local file"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_correct_load(self):
        data = cfg_utils.load_configuration(self.cfg_file)

        ref_data = {
            'ngram': {
                'kwargs': {'header': '@dd', 'order': 3},
                'model': '/mnt/data/ml/qwant/models/ngrams/wikipedia/'\
                         'fr-articles/lm_order3_500kwords_modKN_'\
                         'prune1e-9_frwiki-latest-pages-articles.bin'
            },
            'evaluate': {
                'data': {
                    'input': 'noisy',
                    'file': '/src/tests/spelling/sample-queries.jsonl',
                    'target': 'clean'
                },
                'top': [10, 5, 1]
            },
            'hunspell': {
                'dic': '/mnt/data/ml/qwant/datasets/dictionaries/hunspell/FR/'\
                       'fr_plus_frwiki-latest-pages-articles_'\
                       'voc-top500k-words.dic',
                'aff': '/mnt/data/ml/qwant/datasets/dictionaries/hunspell/'\
                       'FR/fr.aff'
            },
            'spacy': {
                'model': 'fr_core_news_sm',
                'disable': ['ner', 'parser']
            }
        }

        self.assertEqual(ref_data, data)

    def test_bad_load(self):
        with open(self.test_file, 'w') as ostream:
            ostream.write('%sfwhfkjf\n')

        with self.assertRaises(Exception) as context:
            cfg_utils.load_configuration(self.test_file)

        self.assertTrue('Exception encountered' in str(context.exception))

    def test_empty_load(self):
        with self.assertRaises(Exception) as context:
            cfg_utils.load_configuration(self.empty_file)

        self.assertTrue('Empty configuration' in str(context.exception))

    def test_nodict_load(self):
        with open(self.test_file, 'w') as ostream:
            ostream.write('---\n')
            ostream.write('-\n')

        with self.assertRaises(Exception) as context:
            cfg_utils.load_configuration(self.test_file)

        self.assertTrue('Not a dict object stored' in str(context.exception))

    def test_absence(self):
        res1 = cfg_utils.get_missing(['a', 'b'], ['a', 'b', 'c'])
        res2 = cfg_utils.get_missing(['a', 'b'], ['a', 'c', 'd'])
        res3 = cfg_utils.get_missing(['a', 'b'], ['c', 'd', 'e'])

        self.assertEqual([], res1)
        self.assertEqual(['b'], res2)
        self.assertEqual(['a', 'b'], res3)

    def test_no_match(self):
        data = cfg_utils.load_configuration(self.cfg_file)

        with self.assertRaises(Exception) as context:
            cfg_utils.match_keys_structure({}, data)

        self.assertTrue('Given configuration' in str(context.exception))

    def test_match(self):
        data = cfg_utils.load_configuration(self.cfg_file)

        res1 = cfg_utils.match_keys_structure(
            {'model': None, 'kwargs': None, 'header': None, 'order': None},
            data['ngram'])

        res2 = cfg_utils.match_keys_structure(
            {'model': None, 'disable': None},
            data['spacy'])

        res3 = cfg_utils.match_keys_structure(
            {'dic': None, 'aff': None},
            data['hunspell'])

        res4 = cfg_utils.match_keys_structure(
            {
                'data': None, 'file': None, 'input': None,
                'target': None, 'top': None
            },
            data['evaluate'])

        self.assertEqual(None, res1)
        self.assertEqual(None, res2)
        self.assertEqual(None, res3)
        self.assertEqual(None, res4)

    def test_match_keys(self):
        data = cfg_utils.load_configuration(self.cfg_file)

        with self.assertRaises(Exception) as context:
            cfg_utils.match_keys({}, data)

        self.assertTrue('Missing mandatory options' in str(context.exception))

        res = cfg_utils.match_keys(
            {'spacy': None, 'ngram': None, 'hunspell': None, 'evaluate': None},
            data)
        self.assertEqual(None, res)

    def test_expand(self):
        data = cfg_utils.load_configuration(self.cfg_file)
        self.assertEqual('', cfg_utils.expand_to_string(data))
        self.assertEqual(
            'ner parser',
            cfg_utils.expand_to_string(data['spacy']['disable']))
        self.assertEqual(
            '',
            cfg_utils.expand_to_string(data['evaluate']['top']))
        self.assertEqual(
            'a 1 b 2 c 3',
            cfg_utils.expand_to_string([{'a': 1}, {'b': 2}, ['c', 3], 5]))
