import logging
from marisa_trie import RecordTrie
from ccquery.utils import io_utils

class LanguageModel:
    """
    Use the trie-based n-gram language model
    (code inspired from pynlpl's library)

    Focus:
    - fast load the n-gram trie from binary file
    - compute the log-probabilities of n-grams
    - reorder a sequence of n-grams by their log-probabilities
    """

    def __init__(self, path, header="@dd", order=3):
        """Load language model from file"""

        io_utils.check_file_readable(path)

        self.logger = logging.getLogger(__name__)

        self.order = order
        self.model = RecordTrie(header)
        self.model.load(path)

    def _prob(self, ngram):
        """Return probability of given ngram tuple"""
        return self.model[ngram][0][0]

    def _backoff(self, ngram):
        """Return backoff value of a given ngram tuple"""
        return self.model[ngram][0][1]

    def has_word(self, word):
        """Check if given word is known by the model"""
        if word in self.model:
            return True
        return False

    def score_word(self, word):
        """Get the unigram log-probability of given word"""

        try:
            return self._prob(word)
        except KeyError:
            try:
                return self._prob('<unk>')
            except KeyError:
                raise KeyError(
                    "Word {} not found (model has no <unk>)".format(word))

    def _score(self, word, history=None):
        """Get the n-gram's log probability"""

        if not history:
            return self.score_word(word)

        # constrain sequence length up to 'order' words
        lookup = history + (word,)
        if len(lookup) > self.order:
            lookup = lookup[-self.order:]

        try:
            return self._prob(' '.join(lookup))
        except KeyError:
            # not found, back off
            try:
                backoffweight = self._backoff(' '.join(history))
            except KeyError:
                backoffweight = 0
            return backoffweight + self._score(word, history[1:])

    def score_sequence(self, data):
        """
        Compute the log-probability of a given word sequence

        When using a 3-gram language model
            score('manger une pomme') =
                prob('manger') +
                prob('manger une') +
                prob('manger une pomme')

        If the 3-gram 'manger une pomme' is not known by the model
            score('manger une pomme') =
                prob('manger') +
                prob('manger une') +
                backoff('manger une') + prob('une pomme')
        """

        if isinstance(data, str):
            data = tuple(data.split())

        if len(data) == 1:
            return self.score_word(data[0])

        result = 0
        history = ()
        for word in data:
            result += self._score(word, history)
            history += (word,)
        return result

    def score_sentence(self, data, bos='<s>', eos='</s>'):
        """Compute the sum of log-probabilities for given sentence"""
        data = bos + ' ' + data + ' ' + eos
        return self.score_sequence(data)

    def order_sequences(self, sequences):
        """Order the sequences by their n-gram log probabilities"""
        scores = {seq: self.score_sequence(seq) for seq in sequences}
        return sorted(scores.keys(), key=lambda k: scores[k], reverse=True)

    def __getitem__(self, ngram):
        """Allow easy access to n-gram's log probability"""
        return self.score_sequence(ngram)
