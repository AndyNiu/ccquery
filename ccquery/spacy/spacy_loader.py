import logging
import spacy
from ccquery.error import ConfigError

class SpacyLoader:
    """Load and use spacy NLP models"""

    def __init__(self, model, disable=None):
        """Load spacy model and disable pipes if requested"""

        self.logger = logging.getLogger(__name__)

        try:
            self.nlp = spacy.load(model, disable=disable)
        except OSError as exc:
            raise ConfigError("Model {} not found: {}".format(model, exc))

        self.pipeline = [x[0] for x in self.nlp.pipeline]

    def check_pipe(self, pipe):
        """Check if given component is present in the pipeline"""
        return pipe in self.pipeline

    def tokenize(self, text):
        """Tokenize given text and yield each token"""
        doc = self.nlp(text)
        for token in doc:
            yield token

    def str_tokenize(self, text):
        """Tokenize given text and yield each token's content"""
        doc = self.nlp(text)
        for token in doc:
            yield token.text

    def split_and_flag(self, text):
        """
        Tokenize given text.

        Flag to ignore tokens
          - shaped like punctuation, numbers, urls or emails
          - representing named entities
        """

        doc = self.nlp(text)

        tokens, flags = [], []
        for token in doc:
            # ignore white-space tokens ...
            if not token.is_space:
                tokens.append(token.text.lower())
                if token.is_punct \
                        or token.like_num \
                        or token.like_url \
                        or token.like_email \
                        or token.ent_type != 0:
                    flags.append(1)
                else:
                    flags.append(0)
        return tokens, flags
