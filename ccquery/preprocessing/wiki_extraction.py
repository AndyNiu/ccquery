import os
import logging

from ccquery.utils import io_utils, cfg_utils, str_utils
from ccquery.data.json_controller import stream_field
from ccquery.preprocessing import Vocabulary

EXTRACTSCRIPT = "WikiExtractor.py"

class WikiExtraction:
    """
    Extract data from Wikipedia dumps

    Focus:
    - download wikipedia dump
    - decompress wikipedia archive
    - extract content from wikipedia xml file
    - extract sentences from wikipedia content
    - preprocess text
    - store clean wikipedia content
    - filter and store the word vocabulary
    - store the character vocabulary
    """

    def __init__(self):
        """Initialize the wikipedia extractor"""

        self.logger = logging.getLogger(__name__)
        self.chars = None
        self.words = None

    def save_archive(self, input_file, output_file):
        """Download archive and store it locally"""

        self.logger.info(
            "Download wikipedia dump from {} and store it to {}".format(
                input_file, output_file))

        io_utils.create_path(output_file)
        io_utils.download(input_file, output_file)

    def save_xml(self, input_file, output_file):
        """Decompress the archive and store its content to file"""

        self.logger.info(
            "Decompress wikipedia dump from {} and store it to {}".format(
                input_file, output_file))

        io_utils.create_path(output_file)
        io_utils.decompress(input_file, output_file)

    def save_content(self, input_file, output_file, args):
        """Extract plain text from Wikipedia xml file"""

        io_utils.create_path(output_file)
        command = "{} {} {} -o - > {}".format(
            EXTRACTSCRIPT,
            input_file,
            cfg_utils.expand_to_string(args),
            output_file)

        self.logger.info(
            "Extract plain text from Wikipedia "\
            "by executing the command:\n{}".format(command))

        # launch extractor script with given configuration
        os.system(command)

    def save_sentences(self, input_file, output_file, field, **clean_kwargs):
        """Extract and preprocess sentences from Wikipedia jsonl file"""

        self.logger.info(
            "Extract clean sentences from {} and store them to {}".format(
                input_file, output_file))

        io_utils.create_path(output_file)
        with open(output_file, 'w', encoding='utf-8') as ostream:
            for doc in stream_field(input_file, field):
                for sent in str_utils.sentences(doc):
                    sent = str_utils.clean_text(sent, **clean_kwargs)
                    if sent:
                        ostream.write(sent + '\n')

    def load_words(self, input_file):
        """Load words from preprocessed sentences"""
        self.words = Vocabulary(input_file, token='word')

    def plot_word_occurrences(self, output_file, **kwargs):
        """Analyze the word occurrences"""

        if self.words:
            self.words.plot_minoccurrences(output_file, **kwargs)

    def filter_words(self, minocc=None, topn=None):
        """
        Extract most frequent words from preprocessed sentences
        - either keep the words seen minimum 'minocc' times in the corpus
        - or keep the 'topn' most frequent words in the corpus
        """

        if self.words:
            self.words.filter_tokens(minocc=minocc, topn=topn)

    def save_words(self, output_file):
        """Store words to json/txt file"""

        if self.words:
            self.words.save_tokens(output_file)

    def load_chars(self, input_file):
        """Load characters from preprocessed sentences"""
        self.chars = Vocabulary(input_file, token='char')

    def plot_char_occurrences(self, output_file, **kwargs):
        """Analyze the character occurrences"""

        if self.chars:
            self.chars.plot_minoccurrences(output_file, **kwargs)

    def filter_chars(self, minocc=None, topn=None):
        """
        Extract most frequent characters from preprocessed sentences
        - either keep the characters seen minimum 'minocc' times in the corpus
        - or keep the 'topn' most frequent characters in the corpus
        """

        if self.chars:
            self.chars.filter_tokens(minocc=minocc, topn=topn)

    def save_chars(self, output_file):
        """Save the character counts to json file"""

        if self.chars:
            self.chars.save_tokens(output_file)
