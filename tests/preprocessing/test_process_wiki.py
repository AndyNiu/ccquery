import os
import filecmp
import unittest
from ccquery.preprocessing import WikiExtraction
from ccquery.utils import io_utils

class TestWikiProcessing(unittest.TestCase):
    """Test the wiki extraction methods"""

    def setUp(self):
        """Set up local variables"""

        self.extractor = WikiExtraction()
        self.sample = os.path.join(os.path.dirname(__file__), 'sample.bz2')
        self.data = os.path.join(os.path.dirname(__file__), 'sample-corpus.txt')
        self.vocab = os.path.join(os.path.dirname(__file__), 'sample-vocab.txt')

        io_utils.check_file_readable(self.sample)
        io_utils.check_file_readable(self.data)
        io_utils.check_file_readable(self.vocab)

        # temporary files
        self.files = {
            'dld':   os.path.join(os.path.dirname(__file__), 'dld.xml'),
            'xml':   io_utils.change_extension(self.sample, 'xml'),
            'jsonl': io_utils.change_extension(self.sample, 'jsonl'),
            'txt':   io_utils.change_extension(self.sample, 'txt'),
            'wvoc':  io_utils.change_extension(self.sample, 'wvoc.txt'),
            'wplot': io_utils.change_extension(self.sample, 'wvoc.png'),
            'cvoc':  io_utils.change_extension(self.sample, 'cvoc.txt'),
            'cplot': io_utils.change_extension(self.sample, 'cvoc.png'),
        }

    def tearDown(self):
        """Remove temporary files"""
        for file in self.files.values():
            io_utils.delete_file(file)

    def test_sequential_processing(self):
        """Test the all the intermediate wikidump processings"""
        self.execute_fake_download(self.files['dld'])
        self.execute_decompress(self.sample, self.files['xml'])
        self.execute_extract(self.files['xml'], self.files['jsonl'])
        self.execute_sentences(self.files['jsonl'], self.files['txt'])
        self.execute_word_vocabulary(
            self.files['txt'], self.files['wvoc'], self.files['wplot'])
        self.execute_char_vocabulary(
            self.files['txt'], self.files['cvoc'], self.files['cplot'])

    def execute_fake_download(self, fout):
        """Test the download feature"""

        # not a wiki dump
        url = 'https://dumps.wikimedia.org/enwiki/latest/'\
              'enwiki-latest-abstract.xml.gz-rss.xml'

        self.extractor.save_archive(url, fout)

    def execute_decompress(self, fin, fout):
        """Test the decompress feature"""
        self.extractor.save_xml(fin, fout)
        self.assertEqual(os.path.exists(fout), True)
        self.assertEqual(io_utils.count_lines(fout), 366)

    def execute_extract(self, fin, fout):
        """Test the wiki extraction feature"""
        args = [
            '--quiet',
            '--json',
            '--bytes 30G',
            '--processes 2',
            '--no-templates',
            '--filter_disambig_pages',
            '--min_text_length 50',
        ]
        self.extractor.save_content(fin, fout, args)
        self.assertEqual(os.path.exists(fout), True)
        self.assertEqual(io_utils.count_lines(fout), 3)

    def execute_sentences(self, fin, fout):
        """Test the sentence division feature"""
        kwargs = {
            'ignore_digits': True,
            'apostrophe': 'fr',
            'ignore_punctuation': 'noise-a',
            'tostrip': False,
            'keepalnum': True,
        }
        self.extractor.save_sentences(fin, fout, 'text', **kwargs)
        self.assertEqual(os.path.exists(fout), True)
        self.assertEqual(io_utils.count_lines(fout), 111)
        self.assertTrue(
            filecmp.cmp(self.data, fout, shallow=False),
            'Generated corpus different from reference corpus')

    def execute_word_vocabulary(self, fin, fout, pout):
        """Test the vocabulary definition feature"""
        kwargs = {'topn': 500}
        self.extractor.load_words(fin)

        self.extractor.plot_word_occurrences(pout, mins=[1, 2, 3])
        self.assertTrue(os.path.exists(pout))

        self.extractor.filter_words(**kwargs)
        self.extractor.save_words(fout)
        self.assertEqual(os.path.exists(fout), True)
        self.assertEqual(io_utils.count_lines(fout), 500)
        self.assertTrue(
            filecmp.cmp(self.vocab, fout, shallow=False),
            'Generated vocabulary different from reference vocabulary')

    def execute_char_vocabulary(self, fin, fout, pout):
        """Test the vocabulary definition feature"""
        kwargs = {'topn': 20}
        self.extractor.load_chars(fin)

        self.extractor.plot_char_occurrences(pout, mins=[1, 2, 3])
        self.assertTrue(os.path.exists(pout))

        self.extractor.filter_chars(**kwargs)
        self.extractor.save_chars(fout)
        self.assertEqual(os.path.exists(fout), True)
        self.assertEqual(io_utils.count_lines(fout), 20)
