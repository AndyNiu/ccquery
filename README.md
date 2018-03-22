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
