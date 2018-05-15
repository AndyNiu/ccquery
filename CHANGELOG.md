# Changelog

## 0.2.0 - WIP


## 0.1.0 - 15/05/2018
### Added
* process Wikipedia dumps in order to define
    * a word vocabulary
    * a textual corpus for training a n-gram language model
* use SRILM toolkit to train and test a n-gram language model
* build the python trie-based version of the SRILM language model
    * store it in binary file for faster reload
    * enable it to compute the log-probability of word sequences
* use spacy NLP library
    * tokenization and named-entity detection
    * detection of tokens like numbers, punctuation, emails, urls
* use the hunspell tool to generate candidate corrections for misspelled words
    * requires reference .dic and .aff files
    * generate a new .dic file by combining the reference one with a *most frequent words* vocabulary
* combine the information extracted from spacy, hunspell and n-gram language models
    * generate candidate corrections for misspelled tokens
    * re-rank those correction based on their log-probabilities
