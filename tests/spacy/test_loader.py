import unittest
from ccquery.spacy import SpacyLoader

class TestSpacyLoader(unittest.TestCase):
    """Test the performance evaluation of automation corrections"""

    def setUp(self):
        """Set up local variables"""
        self.nlp = SpacyLoader('fr_core_news_sm', disable=['ner'])

    def tearDown(self):
        """Remove temporary variables"""
        del self.nlp

    def test_all_in_one(self):
        """Test all methods at the same time (avoid re-loading model)"""
        self.subtest_bad_load()
        self.subtest_pipeline()
        self.subtest_tokenize()
        self.subtest_split_and_flag()

    def subtest_bad_load(self):
        """Test loading an unknown model"""

        with self.assertRaises(Exception) as context:
            SpacyLoader('unknown')
        self.assertTrue('not found' in str(context.exception))

    def subtest_pipeline(self):
        """Test pipe presence"""

        pipes = ['tokenizer', 'tagger', 'parser', 'ner']
        presence = [self.nlp.check_pipe(pipe) for pipe in pipes]
        self.assertEqual([False, True, True, False], presence)

    def subtest_tokenize(self):
        """Test tokenization"""

        # simple sentence
        sent = 'enregistrer une vidéo sur internet'
        rtokens = sent.split()
        self.assertEqual(rtokens, [str(x) for x in self.nlp.tokenize(sent)])
        self.assertEqual(rtokens, list(self.nlp.str_tokenize(sent)))

    def subtest_split_and_flag(self):
        """Test the tokenizer"""

        queries = [
            'comment rehoindre une force',
            'ascenssion 2019',
            'facebok',
            'éliminer tche vin rouge fraiche sur nappe',
            'fenêtre coulissante alu ou pvc?',
            'au cœur de l\'histoire',
            'quand le citronnier perd ses feuilles?',
            'acteur jumanji 2017',
            '21 boulevard haussmann pages jaunes',
            'carrousel rouge nantes',
        ]

        rtokens = [
            ['comment', 'rehoindre', 'une', 'force'],
            ['ascenssion', '2019'],
            ['facebok'],
            ['éliminer', 'tche', 'vin', 'rouge', 'fraiche', 'sur', 'nappe'],
            ['fenêtre', 'coulissante', 'alu', 'ou', 'pvc', '?'],
            ['au', 'cœur', 'de', 'l\'', 'histoire'],
            ['quand', 'le', 'citronnier', 'perd', 'ses', 'feuilles', '?'],
            ['acteur', 'jumanji', '2017'],
            ['21', 'boulevard', 'haussmann', 'pages', 'jaunes'],
            ['carrousel', 'rouge', 'nantes'],
        ]

        rflags = [
            [0, 0, 0, 0],
            [0, 1],
            [0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 0],
        ]

        tokens = []
        ignore_flags = []
        for query in queries:
            token, flag = self.nlp.split_and_flag(query)
            tokens.append(token)
            ignore_flags.append(flag)

        self.assertEqual(rtokens, tokens)
        self.assertEqual(rflags, ignore_flags)
