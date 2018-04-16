import logging
from ccquery.spacy import SpacyLoader
from ccquery.spelling import HunSpelling
from ccquery.ngram import LanguageModel
from ccquery.utils import str_utils

class B1Correction:
    """
    Automatically correct spelling errors

    Baseline 1
    - use spacy for tokenization and named-entity detection
    - use hunspell for detecting isolated non-word spelling errors
      and suggesting candidate corrections
    - rerank candidates using a n-gram language model
    """

    def __init__(self):
        """Initialize the baseline"""

        self.nlp = None
        self.hunspell = None
        self.ngram = None

        self.logger = logging.getLogger(__name__)

    def load_spacy(self, nlp_model, disable=None):
        """Load the spacy NLP pipelines"""

        self.nlp = SpacyLoader(nlp_model, disable=disable)
        self.logger.info('Loaded spacy NLP model')

    def load_hunspell(self, dic_file, aff_file, extra_dic=None):
        """Load the hunspell analysis"""

        self.hunspell = HunSpelling(dic_file, aff_file, extra_dic=extra_dic)
        self.logger.info('Loaded hunspell checker')

    def load_ngram(self, ngram_model, **kwargs):
        """Load the n-gram language model"""

        self.ngram = LanguageModel(ngram_model, **kwargs)
        self.logger.info('Loaded n-gram language model')

    def correct(self, query, topn=5):
        """Return top candidate corrections for given query"""

        # recover tokens and flags for tokens to ignore by spellchecker
        tokens, flags = self.nlp.split_and_flag(query)

        # recover the list of correction suggestions made by hunspell
        candidates = self.hunspell.correct(tokens, ignore=flags)

        # re-order the candidates list by the n-gram language model
        candidates = self.ngram.order_sequences(candidates)

        # post-process sequences (remove spaces surrounding punctuation marks)
        candidates = [
            str_utils.remove_spaces_apostrophes(s) for s in candidates]

        return candidates[:topn]
