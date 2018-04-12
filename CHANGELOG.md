# Changelog

## 0.1.0 - WIP
* process Wikipedia dumps in order to define
    * a word vocabulary
    * a textual corpus for training a n-gram language model
* use SRILM toolkit to train and test a n-gram language model
* build the python trie-based version of the SRILM language model
    * store it in binary file for faster reload
    * enable it to compute the log-probability of word sequences
