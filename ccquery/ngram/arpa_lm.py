import re
import logging
from marisa_trie import RecordTrie
from ccquery.utils import io_utils

class ArpaLanguageModel:
    """
    Change format of ARPA language model
    (code inspired from pynlpl's library)

    Focus:
    - load pre-computed back-off language model from file in ARPA format
    - build a trie on the entries 'ngram: (logprob, backoff)' (use marisa_trie)
    - store the trie model in binary file (usefull for faster reload)

    Note:
    - might require a lot of memory depending on the size of the language model
    - use only once
    """

    def __init__(self, path):
        """Load ARPA language model from file"""

        io_utils.check_file_readable(path)

        self.logger = logging.getLogger(__name__)
        self.logger.info("Load ARPA model from {}".format(path))

        order = None
        self.total = {}

        data = {}
        with open(path, 'rt', encoding='utf-8') as istream:
            for line in istream:
                line = line.strip()
                if line:
                    if line == '\\data\\':
                        order = 0
                    elif line == '\\end\\':
                        break
                    elif line.startswith('\\') and line.endswith('-grams:'):
                        order = int(re.findall(r"\d+", line)[0])
                        self.logger.info("Processing {}-grams".format(order))
                    elif order == 0 and line.startswith('ngram'):
                        n = int(line[6])
                        count = int(line[8:])
                        self.total[n] = count
                    elif order > 0:
                        fields = line.split('\t')
                        logprob = float(fields[0])
                        ngram = ' '.join(fields[1].split())
                        if len(fields) > 2:
                            backoffprob = float(fields[2])
                        else:
                            backoffprob = 0.0
                        data[ngram] = (logprob, backoffprob)

        self.order = order

        self.logger.info(
            "Loaded a {}-gram LM with {} counts".format(self.order, self.total))

        # handle the prob(<s>) = -99 case
        sos = "<s>"
        if sos in data:
            backoff = data[sos][1]
            data[sos] = (0.0, backoff)

        self.data = RecordTrie("@dd", list(data.items()))
        self.logger.info("Finished storing n-grams under trie structure")

    def save_trie(self, output):
        """Store trie-based n-grams under binary format"""

        self.logger.info(
            "Store trie-based n-grams under binary format in {}".format(output))
        self.data.save(output)
