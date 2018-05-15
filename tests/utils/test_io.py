import os
import unittest
from ccquery.utils import io_utils

class TestIO(unittest.TestCase):
    """Test the input/output utility functions"""

    def setUp(self):
        """Set up local variables"""

        self.cur_dir = os.path.dirname(__file__)
        self.empty_file = os.path.join(os.path.dirname(__file__), '__init__.py')
        self.tmp_file = os.path.join(os.path.dirname(__file__), 'temp_file.xml')
        self.archive = os.path.join(
            os.path.dirname(__file__), '..', 'preprocessing', 'sample.bz2')

    def tearDown(self):
        """Delete local file"""
        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)

    def test_checkups(self):
        self.assertEqual(None, io_utils.check_file_readable(self.empty_file))
        self.assertEqual(None, io_utils.check_folder_readable(self.cur_dir))

        with self.assertRaises(Exception) as context:
            io_utils.check_file_readable('file.txt')
        self.assertTrue('missing or not readable' in str(context.exception))

        with self.assertRaises(Exception) as context:
            io_utils.check_folder_readable('folder')
        self.assertTrue('missing' in str(context.exception))

    def test_create_delete(self):
        io_utils.create_path(self.empty_file)
        io_utils.create_folder(self.cur_dir)

        self.assertEqual(None, io_utils.check_file_readable(self.empty_file))
        self.assertEqual(None, io_utils.check_folder_readable(self.cur_dir))

        cfolder = 'test_folder'
        cfile = os.path.join(cfolder, 'test_file.txt')

        io_utils.create_path(cfile)
        with open(cfile, 'w') as ostream:
            ostream.write('')
        self.assertEqual(None, io_utils.check_file_readable(cfile))

        io_utils.delete_file(cfile)
        with self.assertRaises(Exception) as context:
            io_utils.check_file_readable(cfile)
        self.assertTrue('missing or not readable' in str(context.exception))

        io_utils.delete_folder(cfolder)
        io_utils.create_folder(cfolder)
        self.assertEqual(None, io_utils.check_folder_readable(cfolder))

        io_utils.delete_folder(cfolder)
        with self.assertRaises(Exception) as context:
            io_utils.check_folder_readable(cfolder)
        self.assertTrue('missing' in str(context.exception))

        io_utils.create_path('nofile.txt')

    def test_file(self):
        self.assertEqual('__init__.py', io_utils.filename(self.empty_file))
        self.assertEqual('.py', io_utils.extension(self.empty_file))
        self.assertEqual('__init__', io_utils.basename(self.empty_file))
        self.assertEqual(
            '/src/tests/utils',
            io_utils.dirname('/src/tests/utils/__init__.py'))
        self.assertEqual(
            '/src/tests/utils/__init__',
            io_utils.path_without_ext('/src/tests/utils/__init__.py'))

        self.assertEqual('0.0Bytes', io_utils.filesize(self.empty_file))
        self.assertEqual('11.9KB', io_utils.filesize(self.archive))
        self.assertEqual(0, io_utils.count_lines(self.empty_file))

        self.assertTrue(io_utils.has_extension(self.empty_file, '.py'))
        self.assertFalse(io_utils.has_extension(self.empty_file, '.txt'))

        self.assertEqual(
            '/src/tests/utils/__init__.txt',
            io_utils.change_extension('/src/tests/utils/__init__.py', 'txt'))
        self.assertEqual('', io_utils.change_extension('', 'txt'))

    def test_download(self):
        url = 'https://dumps.wikimedia.org/enwiki/latest/'\
              'enwiki-latest-abstract.xml.gz-rss.xml'

        io_utils.download(url, self.tmp_file)

        with self.assertRaises(Exception) as context:
            io_utils.download('https://not-a-real-file.txt', self.tmp_file)
        self.assertTrue('Exception encountered' in str(context.exception))

    def test_decompress(self):
        io_utils.decompress(self.archive, self.tmp_file)
        self.assertEqual(None, io_utils.check_file_readable(self.tmp_file))

        with self.assertRaises(Exception) as context:
            io_utils.decompress(self.empty_file, self.tmp_file)
        self.assertTrue('not a bz2 archive' in str(context.exception))
