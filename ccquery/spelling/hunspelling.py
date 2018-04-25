from itertools import product
from hunspell import HunSpell
from ccquery.utils import io_utils

class HunSpelling:
    """
    Use the hunspell tool to detect isolated non-word spelling errors
    and to suggest candidate corrections
    """

    def __init__(self, dic_file, aff_file, extra_dic=None):
        """
        Load the dictionary and affix files for spell checking.
        Allow adding an extra dictionary.
        """

        io_utils.check_file_readable(dic_file)
        io_utils.check_file_readable(aff_file)

        self.hunspell = HunSpell(dic_file, aff_file)
        if extra_dic:
            io_utils.check_file_readable(extra_dic)
            self.hunspell.add_dic(extra_dic)

    def is_misspelled(self, word):
        """Check if given word is misspelled"""
        return not self.hunspell.spell(word)

    def add_word(self, word):
        """Add new word into hunspell's dictionary"""
        if word:
            self.hunspell.add(word)

    def add_words(self, words):
        """Add new words into hunspell's dictionary"""
        if not isinstance(words, list):
            return
        for word in words:
            self.add_word(word)

    def add_extra_dictionary(self, dic_file):
        """Add an extra dictionary to the current instance"""
        io_utils.check_file_readable(dic_file)
        self.hunspell.add_dic(dic_file)

    def remove_word(self, word):
        """Remove word from hunspell's dictionary"""
        self.hunspell.remove(word)

    def remove_words(self, words):
        """Remove words from hunspell's dictionary"""
        if not isinstance(words, list):
            return
        for word in words:
            self.remove_word(word)

    def get_suggestions(self, word):
        """Return correction suggestions"""

        suggestions = []
        for sgt in self.hunspell.suggest(word):
            sgt = sgt.replace('-', ' ')
            if not sgt in suggestions:
                suggestions.append(sgt)
        return suggestions

    def correct(self, query, ignore=None, topn=None):
        """
        Return top candidate corrections for given query.
        The ignore flag can allow ignoring certain words
        (e.g. named entities)
        """

        if not isinstance(query, list):
            query = query.split()

        if ignore is None:
            ignore = [0] * len(query)

        solutions = []

        for i, token in enumerate(query):
            if token.isalpha() \
                    and not self.hunspell.spell(token) \
                    and not ignore[i]:

                suggestions = self.get_suggestions(token)

                if suggestions:
                    solutions.append(suggestions)
                else:
                    solutions.append([token])
            else:
                solutions.append([token])

        # merge solutions
        candidates = [' '.join(sol) for sol in product(*solutions)]

        return candidates[:topn]
