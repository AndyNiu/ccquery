import string
import logging
import unicodedata
import regex

LOGGER = logging.getLogger(__name__)
DIGITMAP = {ord(str(x)):' ' for x in range(10)}

CHARSET = {
    'digits':        regex.compile(r"\d"),
    'punctuation':   regex.compile(r"\p{posix_punct}"),
    'punctuation-a': regex.compile(r"(?V1)[\p{posix_punct}--']"),
    'punctuation-s': regex.compile(r"(?V1)[\p{posix_punct}--'\"\-_\.,]"),
    'noise':         regex.compile(r"[^\p{Latin}]"),
    'noise-a':       regex.compile(r"[^\p{Latin}']"),
    'noise-s':       regex.compile(r"[^\p{Latin}'\"_\.-]"),
}

def char_category(char):
    """Return the character's unicode category"""
    return unicodedata.category(char)[0]

def char_name(char):
    """Return the character's unicode alphabet name"""
    try:
        return unicodedata.name(char).split()[0]
    except ValueError:
        LOGGER.warning("Character {} has unknown unicode name".format(char))
        return None

def check_char_alphabet(char, alphabet='LATIN'):
    """Check if given character is a valid 'alphabet' character"""

    if char.isdigit() \
            or char in string.punctuation \
            or char_category(char) == 'P':
        return True

    name = char_name(char)
    return name == alphabet or name == 'REPLACEMENT'

def check_text_alphabet(text, alphabet='LATIN'):
    """Check if given text presents only valid 'alphabet' characters"""
    return all(check_char_alphabet(char, alphabet) for char in text)

def check_alphabet(text, alphabet='LATIN'):
    """Check if given text presents only valid 'alphabet' characters"""
    if len(text) == 1:
        return check_char_alphabet(text, alphabet)
    return check_text_alphabet(text, alphabet)

def get_characters(text, alphabet='LATIN'):
    """
    Prepare the data for character-based processing
    - ignore characters from unwanted alphabet
    - return list of characters
    """

    chars = []
    for char in text:
        if check_alphabet(char, alphabet):
            chars.append(char)
    return chars

def check_valid_word(word):
    """Valid word contains only letters and apostrophes"""
    if not word:
        return False
    if word.isalpha():
        return True
    for char in word:
        if not(char.isalpha() or char == "'"):
            return False
    return True

def get_words(text, alphabet='LATIN', ignore='noise-a', lowercase=True):
    """
    Prepare the data for word-based processing
    - ignore numbers
    - ignore punctuation marks (excluding the inside-word apostrophe)
    - ignore tokens presenting characters from unwanted alphabet
    - return list of words
    """

    ctext = regex.sub(CHARSET[ignore], ' ', text)

    if lowercase:
        ctext = ctext.lower()

    words = []
    for word in ctext.split():
        if check_alphabet(word, alphabet):
            word = word.strip(string.punctuation)
            if check_valid_word(word):
                words.append(word)
    return words

def clean_text(
        text, alphabet='LATIN', lowercase=True,
        ignore_digits=False, ignore_punctuation=None,
        tostrip=False, keepalnum=False):
    """
    Prepare the data for word-based processing
    - ignore numbers if requested
    - ignore punctuation marks if requested
    - ignore tokens presenting characters from unwanted alphabet
    - return string
    """

    ctext = text
    if ignore_digits:
        ctext = ctext.translate(DIGITMAP)

    if ignore_punctuation:
        ctext = regex.sub(CHARSET[ignore_punctuation], ' ', ctext)

    if lowercase:
        ctext = ctext.lower()

    ntext = ''
    for word in ctext.split():
        if check_alphabet(word, alphabet):
            if tostrip:
                word = word.strip(string.punctuation)
            if keepalnum:
                if word.isalnum() or "'" in word:
                    ntext += word + ' '
            else:
                ntext += word + ' '
    return ntext.strip()
