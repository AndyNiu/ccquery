import logging
from ccquery.error import ConfigError
from ccquery.utils import io_utils
from ccquery.data import text_controller

class VocMix:
    """
    Combine an external .dic hunspell dictionary
    with a .txt word-based personal dictionary

    Two possible combinations
    - union
        - create a new .dic hunspell dictionary
            keep only rules associated to words seen in the personal dictionary
            add remaining words from the personal dictionary (without any rules)
            adjust the header with the count of tokens within the dictionary
        - hunspell will further use
            the new combined .dic file
            the reference .aff file
    - intersection
        - create a new .dic hunspell dictionary
            keep only rules associated to words seen in the personal dictionary
            adjust the header with the count of tokens within the dictionary
        - create a new extra .dic hunspell dictionary
            store in it every word from the personal dictionary
            adjust the header with the count of tokens within the dictionary
        - hunspell will further use
            the new combined .dic file
            the reference .aff file
            the new extra .dic file
    """

    def __init__(self, hunspell_file, personal_file):
        """Read contents of both vocabularies"""

        self.logger = logging.getLogger(__name__)

        io_utils.check_file_readable(hunspell_file)
        io_utils.check_file_readable(personal_file)

        # load external hunspell dictionary
        self.hdict = text_controller.load(hunspell_file)

        # load personal dictionary
        self.pdict = text_controller.load(personal_file)

        # initialize the combined content
        self.mix_content = None

    def combine_dictionaries(self, method):
        """Combine the dictionaries using the union or intersection approach"""

        self.logger.info(
            "Combine the dictionaries using the {} approach".format(method))

        if method == 'union':
            self._process_union()
        elif method == 'intersection':
            self._process_intersection()
        else:
            raise ConfigError(
                "Unknown mix approach: {}"\
                "Available options: [union, inersection]".format(method))

    def _process_union(self):
        """Combine the dictionaries using the union approach"""

        processed_words = {}
        self.mix_content = [self.hdict[0]]

        # keep rules for shared words
        for i in range(1, len(self.hdict)):
            tokens = self.hdict[i].split('/')
            word = tokens[0].lower()

            if word in self.pdict:
                processed_words[word] = 1

                if len(tokens) == 1:
                    self.mix_content.append(word)
                else:
                    self.mix_content.append("{}/{}".format(word, tokens[1]))

        # add words from personal dictionary
        for word in sorted(self.pdict):
            if not word in processed_words:
                self.mix_content.append(word)

        # update the number of tokens in the dictionary
        self.mix_content[0] = len(self.mix_content) - 1

        # order words
        self.mix_content = self.mix_content[0:1] + sorted(self.mix_content[1:])

        self.logger.info(
            "Generated a new dictionary of {} words".format(
                len(self.mix_content) - 1))

    def _process_intersection(self):
        """Combine the dictionaries using the intersection approach"""

        self.mix_content = [self.hdict[0]]

        # keep rules for shared words
        for i in range(1, len(self.hdict)):
            tokens = self.hdict[i].split('/')
            word = tokens[0].lower()

            if word in self.pdict:
                if len(tokens) == 1:
                    self.mix_content.append(word)
                else:
                    self.mix_content.append("{}/{}".format(word, tokens[1]))

        # update the number of tokens in the dictionary
        self.mix_content[0] = len(self.mix_content) - 1

        # order words
        self.mix_content = self.mix_content[0:1] + sorted(self.mix_content[1:])

        self.logger.info(
            "Generated a new dictionary of {} words".format(
                len(self.mix_content) - 1))

    def save_combined_dictionary(self, output):
        """Store combined hunspell dictionary to file"""

        with open(output, 'w', encoding='utf-8') as ostream:
            for line in self.mix_content:
                ostream.write(str(line) + '\n')

    def save_personal_dictionary(self, output):
        """Store personal dictionary under hunspell format"""

        # add header of word count
        with open(output, 'w', encoding='utf-8') as ostream:
            ostream.write(str(len(self.pdict)) + '\n')
            for word in sorted(self.pdict):
                ostream.write(word + '\n')
