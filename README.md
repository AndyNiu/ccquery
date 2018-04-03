# Automatic query correction & completion project 

## Description

### Define a baseline for query correction

* tokenize text into words (use spacy or a "naive" tokenization)
* use an existing tool for isolated non-word detection and correction (e.g. hanspell)
* rerank candidates by using a probabilistic n-gram language model (LM)

## Usage

### Process wikipedia dumps

Complete process to
* download a .bz2 wikipedia dump file
* decompress the archive
* extract plain text from wikipedia xml file (using the [WikiExtractor.py](https://github.com/attardi/wikiextractor) script)
* split text into sentences and preprocess them
    * lowercase text
    * remove digits
    * remove punctuation marks
    * remove non Latin characters
    * \[*FIXME*\]: uses the external [regex](https://pypi.python.org/pypi/regex/) library, therefore it's quite slow
* count the number of occurrences of tokens (words and characters)
* plot the count and coverage of tokens with respect to a minimum number of occurrences filter
* filter the list of words with respect to their number of occurrences

As a result, this process allows us to define
* a word vocabulary
* the textual corpus needed to train a n-gram LM

```bash
$ scripts/prepare_wikipedia -h
usage: prepare_wikipedia [-h] conf

Download, decompress, extract and clean wikipedia dump data

positional arguments:
    conf        input config file (yml)

optional arguments:
    -h, --help  show this help message and exit
```

### Train n-gram language models

Use the [SRILM](http://www.speech.sri.com/projects/srilm/) toolkit to
* generate n-gram counts based on a word vocabulary and a sentence-per-line corpus
* estimate an open-class language model using the modified Knesser-Ney smoothing technnique

The resulting language model will allow us to compute the log-probability of a sequence of words.

```bash
$ scripts/train_ngram_lm -h
Objective: train a probabilistic n-gram language model

Usage:   scripts/train_ngram_lm <yaml_config_file>
Example: scripts/train_ngram_lm conf/model/config_train_lm_wiki-fr.yml
```


## Docker execution

### Process wikipedia dumps 

```bash
$ docker-compose run --rm devel \
    scripts/prepare_wikipedia \
    conf/data/config_download_clean_wiki-fr.yml
```

Configuration

```yaml
---
url: https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2
output: /mnt/data/ml/qwant/datasets/wikipedia/fr-articles/
args:
    - --quiet
    - --json
    - --bytes 30G
    - --processes 2
    - --no-templates
    - --filter_disambig_pages
    - --min_text_length 50
preprocessing:
    ignore_digits: True
    apostrophe: fr
    ignore_punctuation: noise-a
    tostrip: True
    keepalnum: True
word_filter:
    topn: 500000
plot_format: png
word_plot:
    mins: [1, 2, 3, 5, 10, 100]
    left_lim: [0, 3000000]
    right_lim: [95, 100.4]
char_plot:
    mins: [1, 2, 3, 5, 10, 100, 1000, 10000, 100000]
    left_lim: [0, 750]
    right_lim: [99.5, 100.04]
```

Output

```
INFO [2018-03-28 08:54:06,878] [ccquery] Download wikipedia dump
INFO [2018-03-28 08:54:06,878] [ccquery.preprocessing.wiki_extraction] Download wikipedia dump from
    https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2
    and store it to frwiki-latest-pages-articles.bz2

INFO [2018-03-28 09:26:49,427] [ccquery] Decompress data
INFO [2018-03-28 09:26:49,427] [ccquery.preprocessing.wiki_extraction] Decompress wikipedia dump from
    frwiki-latest-pages-articles.bz2
    and store it to frwiki-latest-pages-articles.xml

INFO [2018-03-28 09:36:11,000] [ccquery] Extract plain text
INFO [2018-03-28 09:36:11,032] [ccquery.preprocessing.wiki_extraction] Extract plain text from Wikipedia by executing the command:
    WikiExtractor.py \
        frwiki-latest-pages-articles.xml \
        --quiet \
        --json \
        --bytes 30G \
        --processes 2 \
        --no-templates \
        --filter_disambig_pages \
        --min_text_length 50 \
        -o - > frwiki-latest-pages-articles.jsonl

INFO [2018-03-28 10:47:31,153] [ccquery] Extract clean sentences
INFO [2018-03-28 10:47:31,153] [ccquery.preprocessing.wiki_extraction] Extract clean sentences from
    frwiki-latest-pages-articles.jsonl
    and store them to frwiki-latest-pages-articles.txt

INFO [2018-03-28 11:53:00,139] [ccquery] Process words
INFO [2018-03-28 11:56:05,278] [ccquery.preprocessing.vocabulary] Read 2,496,898 words with 587,893,490 occurrences
INFO [2018-03-28 11:56:05,279] [ccquery] Plot word occurrences
INFO [2018-03-28 11:56:06,886] [ccquery.preprocessing.vocabulary] Saved histogram on word occurrences under
    frwiki-latest-pages-articles_words.png
INFO [2018-03-28 11:56:06,886] [ccquery] Filter words with respect to number of occurrences
INFO [2018-03-28 11:56:08,198] [ccquery.preprocessing.vocabulary] Saved
    500,000 words out of 2,496,898
    (20.02% unique words, 99.25% coverage of word occurrences)
INFO [2018-03-28 11:56:08,260] [ccquery] Save word vocabulary under json and txt format
INFO [2018-03-28 11:56:09,639] [ccquery.preprocessing.vocabulary] Saved word counts under
    frwiki-latest-pages-articles_voc-topn=500000-words.json
INFO [2018-03-28 11:56:09,817] [ccquery.preprocessing.vocabulary] Saved word counts under
    frwiki-latest-pages-articles_voc-topn=500000-words.txt

INFO [2018-03-28 11:56:09,817] [ccquery] Process characters
INFO [2018-03-28 12:04:21,046] [ccquery.preprocessing.vocabulary] Read 640 chars with 3,370,474,793 occurrences
INFO [2018-03-28 12:04:21,046] [ccquery] Plot character occurrences
INFO [2018-03-28 12:04:21,217] [ccquery.preprocessing.vocabulary] Saved histogram on char occurrences under
    frwiki-latest-pages-articles_chars.png
INFO [2018-03-28 12:04:21,217] [ccquery] Save character vocabulary under json and txt format
INFO [2018-03-28 12:04:21,219] [ccquery.preprocessing.vocabulary] Saved char counts under
    frwiki-latest-pages-articles_voc-chars.json
INFO [2018-03-28 12:04:21,219] [ccquery.preprocessing.vocabulary] Saved char counts under
    frwiki-latest-pages-articles_voc-chars.txt

INFO [2018-03-28 12:04:21,219] [ccquery] Finished.
```

The plot on the word occurrences  
![Word occurrences](data/frwiki-latest-pages-articles_words.png)

The plot on the character occurrences  
![Character occurrences](data/frwiki-latest-pages-articles_chars.png)

### Train n-gram language models

```bash
$ docker-compose run --rm srilm \
    scripts/train_ngram_lm \
    conf/model/config_train_lm_wiki-fr.yml
```

Configuration

```yaml
---
order: 3
vocab: /mnt/data/ml/qwant/datasets/wikipedia/fr-articles/frwiki-latest-pages-articles_voc-topn=500000-words.txt
corpus: /mnt/data/ml/qwant/datasets/wikipedia/fr-articles/frwiki-latest-pages-articles.txt
smoothing: -gt1min 0 -kndiscount2 -gt2min 0 -interpolate2 -kndiscount3 -gt3min 0 -interpolate3
pruning: 1e-9
counts: /mnt/data/ml/qwant/models/ngrams/wikipedia/fr-articles/counts_order3_500kwords_frwiki-latest-pages-articles.txt
model: /mnt/data/ml/qwant/models/ngrams/wikipedia/fr-articles/lm_order3_500kwords_modKN_prune1e-9_frwiki-latest-pages-articles.arpa
```

Output

```bash
Launch n-gram counting
    ngram-count \
        -order 3 \
        -text frwiki-latest-pages-articles.txt \
        -unk -vocab frwiki-latest-pages-articles_voc-topn=500000-words.txt \
        -sort -write counts_order3_500kwords_frwiki-latest-pages-articles.txt \
        -debug 2

29,588,580 sentences, 587,893,490 words, 4,423,341 OOVs
Finished at 13:05:38, after 300 seconds

Launch LM training
    make-big-lm \
        -order 3 \
        -unk -read counts_order3_500kwords_frwiki-latest-pages-articles.txt \
        -name aux -lm lm_order3_500kwords_modKN_prune1e-9_frwiki-latest-pages-articles.arpa \
        -gt1min 0 -kndiscount2 -gt2min 0 -interpolate2 -kndiscount3 -gt3min 0 -interpolate3 \
        -prune 1e-9 \
        -debug 2

using ModKneserNey for 1-grams
using ModKneserNey for 2-grams
using ModKneserNey for 3-grams
warning: distributing 0.000372689 left-over probability mass over all 500002 words

discarded       1 2-gram contexts containing pseudo-events
discarded  454422 3-gram contexts containing pseudo-events

pruned    3254800 2-grams
pruned   88871145 3-grams

writing    500003 1-grams
writing  34634795 2-grams
writing  63960504 3-grams

Finished at 13:34:32, after 1734 seconds

Generated a model of 2.9G
```
