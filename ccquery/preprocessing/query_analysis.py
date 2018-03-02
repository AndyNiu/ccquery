import json
import logging
from collections import defaultdict

from ccquery.error import ConfigError
from ccquery.utils import io_utils, str_utils, plot_utils
import ccquery.data

def check_valid_token(token, tokens):
    """Check if the given token argument is valid"""
    if token not in tokens:
        raise ConfigError(
            "Unknown token type {}. Expected {}".format(token, tokens))

def load_reader(path, **kwargs):
    """Load the right reader for the file / data type"""

    if path.endswith('.txt'):
        return ccquery.data.text_controller.stream(path)
    elif path.endswith('.jsonl'):
        return ccquery.data.json_controller.stream_field(path, **kwargs)
    elif path.endswith('.csv'):
        return ccquery.data.csv_controller.stream_field(path, **kwargs)

    raise ConfigError(
        "Unknown file extension {}. Expected [txt, jsonl, csv]".format(
            io_utils.extension(path)))

def display(counts):
    """Pretty display for word/char counts"""

    maxlen = max(len(str(token)) for token, _ in counts)
    maxfreq = max(freq for _, freq in counts)
    maxfreq = len(str(maxfreq)) + 2

    shape = ''
    for token, freq in counts:
        shape += "{:<{w1}} {:>{w2}}\n".format(
            token, freq, w1=maxlen, w2=maxfreq)
    return shape


class QueryAnalysis:
    """
    Analyze the use of characters and words within queries.

    Focus:
    - recover the list of characters used within queries
    - recover the list of words used within queries
    - recover and plot the character counts per query
    - recover and plot the word counts per query
    - recover the maximum number of characters within queries
    - recover the maximum number of words within queries
    """

    def __init__(self, path, token='char', **kwargs):
        """
        Initialize:
        - load data from file at given path
        - consider only the data under 'field'
        - process the requested type of tokens
        """

        check_valid_token(token, ['char', 'word'])

        self.logger = logging.getLogger(__name__)

        self.reader = load_reader(path, **kwargs)
        self.field = kwargs.get('field', 'Sentences')

        self.token = token
        self.nqueries = 0

        self.data = defaultdict(lambda: 0)
        self.length = defaultdict(lambda: 0)
        self.max_length = 0

    def analyze_chars(self, cleaner=None):
        """Analyze character use in queries"""

        self.nqueries = 0
        for entry in self.reader:
            self.nqueries += 1

            if cleaner:
                char_cleaner = getattr(str_utils, cleaner)
                entry = char_cleaner(entry)

            for char in entry:
                self.data[char] += 1
            self.length[len(entry)] += 1

        self.max_length = max(self.length.keys())

    def analyze_words(self, cleaner=None):
        """Analyze word use in queries"""

        self.nqueries = 0
        for entry in self.reader:
            self.nqueries += 1

            if cleaner:
                word_cleaner = getattr(str_utils, cleaner)
                words = word_cleaner(entry)
            else:
                words = entry.split()

            for word in words:
                self.data[word] += 1
            self.length[len(words)] += 1

        self.max_length = max(self.length.keys())

    def analyze_text(self, cleaner=None):
        """Analyze character and word use in queries"""

        if self.token == 'char':
            self.analyze_chars(cleaner)
        else:
            self.analyze_words(cleaner)

    def plot_query_length(self, output):
        """Draw the bars for query's length in number of words/chars"""

        plot_utils.length_plot(
            output,
            self.length,
            title="Analyzed the query length of {:,} queries".format(
                self.nqueries),
            xlabel="Number of {}s".format(self.token),
            ylabel='Frequency')

        self.logger.info(
            "The queries have the following lengths in number of {}s:\n{}"\
            .format(self.token, display(list(self.length.items()))))
        self.logger.info(
            "Saved histogram on the query length under\n{}".format(output))

    def plot_minoccurrences(self, output, mins, left_lim=None, right_lim=None):
        """Plot the occurrences histogram for characters"""

        ntokens = sum(self.data.values())
        plot_utils.occurrences_plot(
            output,
            list(self.data.values()),
            mins,
            left_lim=left_lim,
            right_lim=right_lim,
            title="'{}' dataset has {:,} unique {}s, {:,} in total".format(
                self.field, len(self.data), self.token, ntokens),
            xlabel="Minimum number of occurrences of {}s".format(self.token),
            ylabel="Number of {}s".format(self.token))

        self.logger.info(
            "Saved histogram on char occurrences under\n{}".format(output))

    def save_tokens(self, output):
        """Save the counts on characters / words"""

        io_utils.create_path(output)
        with open(output, 'w', encoding='utf-8') as ostream:
            json.dump(
                self.data,
                ostream, ensure_ascii=False, indent=4, sort_keys=True)

    def info_tokens(self):
        """Display the analysis on the use of characters / words"""

        self.logger.info(
            "Queries have at most {} {}s".format(self.max_length, self.token))

        self.logger.info(
            "Queries make use of {} unique {}s ({} in total)".format(
                len(self.data), self.token, sum(self.data.values())))

        if self.token == 'char':
            self.logger.info("List of unique {}s: {}".format(
                self.token, ''.join(sorted(self.data.keys()))))

        if len(self.data) < 200:
            sample = sorted(
                self.data.items(), key=lambda x: x[1], reverse=True)
        else:
            sample = sorted(
                self.data.items(), key=lambda x: x[1], reverse=True)[:100]

        self.logger.info(
            "Frequency per {}s\n{}".format(self.token, display(sample)))
