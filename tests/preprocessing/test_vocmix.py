import os
import json
import filecmp
import unittest
from ccquery.data import text_controller
from ccquery.utils import io_utils
from ccquery.preprocessing import VocMix

class TestVocab(unittest.TestCase):
    """Test the mix of two hunspell dictionaries"""

    def setUp(self):
        """Set up local variables"""

        self.voc1 = os.path.join(
            os.path.dirname(__file__), '..', 'spelling', 'index.dic')
        self.voc2 = os.path.join(os.path.dirname(__file__), 'sample-vocab.txt')

        self.combi = os.path.join(os.path.dirname(__file__), 'combined.dic')
        self.newvoc = os.path.join(os.path.dirname(__file__), 'hformat.dic')

        self.with_rules = os.path.join(os.path.dirname(__file__), 'wrules.dic')
        self.rem_words = os.path.join(os.path.dirname(__file__), 'rwords.dic')

    def tearDown(self):
        """Delete temporary files"""
        io_utils.delete_file(self.combi)
        io_utils.delete_file(self.newvoc)
        io_utils.delete_file(self.with_rules)
        io_utils.delete_file(self.rem_words)

    def test_bad_mix(self):
        """Test an unknown combination of words from two dictionaries"""

        vmix = VocMix(self.voc1, self.voc2)
        with self.assertRaises(Exception) as context:
            vmix.combine_dictionaries('bad')
        self.assertTrue('Unknown mix approach' in str(context.exception))

    def test_union_mix(self):
        """Test the union of words from two dictionaries"""

        vmix = VocMix(self.voc1, self.voc2)
        vmix.combine_dictionaries('union')
        vmix.save_combined_dictionary(self.combi)

        self.assertTrue(
            filecmp.cmp(self.combi, self.voc1, shallow=False),
            'Generated vocabulary different from reference vocabulary')

    def test_intersection_mix(self):
        """Test the intersection of words from two dictionaries"""

        vmix = VocMix(self.voc1, self.voc2)
        vmix.combine_dictionaries('intersection')
        vmix.save_combined_dictionary(self.combi)
        vmix.save_personal_dictionary(self.newvoc)

        self.assertTrue(
            filecmp.cmp(self.newvoc, self.voc1, shallow=False),
            'Generated vocabulary different from reference vocabulary')

    def test_intersection_mix_2(self):
        """Test the intersection mix with rules"""

        # include words with rules into the hunspell dictionary and store it
        words = text_controller.load(self.voc1)

        nwords = words.copy()
        rwords = ['angle', 'carrière', 'dimensions']
        for word in rwords:
            index = nwords.index(word)
            nwords[index] = "{}/S*".format(word)

        with open(self.with_rules, 'w', encoding='utf-8') as ostream:
            for word in nwords:
                ostream.write("{}\n".format(word))

        # test intersection
        vmix = VocMix(self.with_rules, self.voc2)
        vmix.combine_dictionaries('intersection')
        vmix.save_combined_dictionary(self.combi)

        self.assertTrue(
            filecmp.cmp(self.combi, self.with_rules, shallow=False),
            'Generated vocabulary different from reference vocabulary')

    def test_union_mix_2(self):
        """Test the union mix with a larger vocabulary"""

        # exclude words from hunspell dictionary (force adding new words)
        # include words with rules
        words = text_controller.load(self.voc1)
        rwords1 = ['angle', 'carrière', 'dimensions']
        rwords2 = ['abstrait', 'algèbre']

        nwords = [w for w in words if w not in rwords1]
        nwords[0] = len(words) - 1

        for word in rwords2:
            index = nwords.index(word)
            nwords[index] = "{}/S*".format(word)

        with open(self.rem_words, 'w', encoding='utf-8') as ostream:
            for word in nwords:
                ostream.write("{}\n".format(word))

        # test union
        vmix = VocMix(self.rem_words, self.voc2)
        vmix.combine_dictionaries('union')
        vmix.save_combined_dictionary(self.combi)

        self.assertEqual(len(vmix.mix_content), len(vmix.pdict) + 1)
