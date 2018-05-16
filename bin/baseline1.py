#!/usr/bin/python3

import os
import sys
import time
import logging
from functools import lru_cache
from flask import Flask, render_template, request, jsonify

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(lib_path)

from ccquery import define_level
from ccquery.spelling import B1Correction

#==================================================
# Configuration
#==================================================

# change logging level
define_level(logging.ERROR)

form_template = 'form.html'

if len(sys.argv) == 1:
    file_config = 'baseline1.cfg'
else:
    file_config = sys.argv[1]


#==================================================
# Initialize Flask API
#==================================================

app = Flask(__name__)
app.config.from_pyfile(file_config)
model_config = app.config['CCQUERY']

#==================================================
# Load models
#==================================================

ctool = B1Correction()
ctool.load_spacy(
    model_config['spacy']['model'],
    model_config['spacy'].get('disable'))
ctool.load_hunspell(
    model_config['hunspell']['dic'],
    model_config['hunspell']['aff'],
    model_config['hunspell'].get('extra'))
ctool.load_ngram(
    model_config['ngram']['model'],
    **model_config['ngram'].get('kwargs'))

#==================================================
# Define API
#==================================================

@lru_cache()
def autocorrect(query, topn=1):
    corrections = ctool.correct(query, topn)
    if topn == 1:
        return corrections[0]
    return corrections

@app.route('/', methods=['GET', 'POST'])
def index():
    bm = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    if bm == 'text/html' and request.method == 'GET':
        return render_template(form_template)

    if bm == 'text/html':
        noisy_query = request.form['query']
    elif bm == 'application/json':
        noisy_query = request.args['query']
    else:
        return '', 406

    tstart = time.monotonic()
    clean_query = autocorrect(noisy_query)
    clean_time = round(time.monotonic() - tstart, 3)

    response = {
        "query": noisy_query,
        "clean_query": clean_query,
        "clean_time": clean_time}

    if bm == 'text/html':
        return render_template(form_template, **response)
    elif bm == 'application/json':
        return jsonify(**response)

#==================================================
# Run API
#==================================================

if __name__ == '__main__':
    app.run()
