import json
import logging
from collections import defaultdict

from ccquery.error import ConfigError
from ccquery.utils import io_utils, plot_utils

class Vocabulary:
    """
    Analyze the use of tokens (characters or words) within a data set

    Focus:
    - recover the list of tokens
    - filter the list of tokens by number of occurrences
    - plot the token occurrences coverage
    """

    def __init__(self, path=None, counts=None, token='word'):
        """Load tokens from path or from a counts dictionary"""

        if token != 'word' and token != 'char':
            raise ConfigError("Method expects a 'word' or a 'char' token")

        self.logger = logging.getLogger(__name__)
        self.token = token

        if path and isinstance(path, str):
            self.tokens = defaultdict(lambda: 0)
            self.occurrences = 0

            io_utils.check_file_readable(path)
            with open(path, 'r', encoding='utf-8') as istream:
                for line in istream:
                    if token == 'word':
                        for word in line.split():
                            self.occurrences += 1
                            self.tokens[word] += 1
                    elif token == 'char':
                        for char in line.strip():
                            self.occurrences += 1
                            self.tokens[char] += 1

            self.logger.info("Read {:,} {}s with {:,} occurrences".format(
                len(self.tokens), self.token, self.occurrences))

        elif counts and isinstance(counts, dict):
            self.tokens = counts.copy()
            self.occurrences = sum(counts.values())

            self.logger.info("Loaded {:,} {}s with {:,} occurrences".format(
                len(self.tokens), self.token, self.occurrences))

        else:
            raise ConfigError('Method expects a file path or a dictionary')


    def filter_tokens(self, minocc=None, topn=None):
        """
        Extract most frequent tokens
        - either keep the tokens seen minimum 'minocc' times
        - or keep the 'topn' most frequent tokens
        """

        ref_ntokens = len(self.tokens)
        ref_nocc = self.occurrences

        if not minocc and not topn:
            raise ConfigError(
                "Method expects either a 'minocc' or a 'topn' argument")

        if minocc:
            new_tokens = {k: v for k, v in self.tokens.items() if v >= minocc}
            self.tokens = new_tokens
        elif topn:
            new_tokens = sorted(
                self.tokens.items(), key=lambda x: (-x[1], x[0]))[:topn]
            self.tokens = dict(new_tokens)

        self.occurrences = sum(self.tokens.values())

        new_ntokens = len(self.tokens)
        new_nocc = self.occurrences

        self.logger.info(
            "Saved {:,} {token}s out of {:,} "\
            "({:.2%} unique {token}s, {:.2%} coverage of {token} occurrences)"
            .format(
                new_ntokens,
                ref_ntokens,
                1.0 * new_ntokens / ref_ntokens,
                1.0 * new_nocc / ref_nocc,
                token=self.token))

    def save_tokens(self, output):
        """Save the token counts to json file"""

        io_utils.create_path(output)

        if output.endswith('.json'):
            # save words and frequencies under json file
            self.logger.info("Save {} counts in json file".format(self.token))
            with open(output, 'w', encoding='utf-8') as ostream:
                json.dump(
                    self.tokens,
                    ostream, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            # save the list of words under text file
            self.logger.info("Save {}s in text file".format(self.token))
            with open(output, 'w', encoding='utf-8') as ostream:
                for token in sorted(self.tokens.keys()):
                    ostream.write(token + '\n')

    def plot_minoccurrences(
            self, output, mins, left_lim=None, right_lim=None, **kwargs):
        """Plot the token occurrences histogram"""

        self.logger.info(
            "Save histogram on {} occurrences".format(self.token))

        plot_utils.occurrences_plot(
            output,
            list(self.tokens.values()),
            mins,
            left_lim=left_lim,
            right_lim=right_lim,
            **kwargs,
            title="Dataset has {:,} unique {}s, {:,} in total".format(
                len(self.tokens), self.token, self.occurrences),
            xlabel="Minimum number of occurrences of {}s".format(self.token),
            ylabel="Number of {}s".format(self.token))
