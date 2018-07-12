# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys
import codecs
import argparse
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import spotipy
import time
import sys
import logging
import lyricwikia
import pprint
from utils_tfidf import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
import nltk
import textblob
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics.pairwise import linear_kernel

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
log_filename = os.path.join(ROOT_DIR, "log/" + os.path.splitext(os.path.basename(__file__))[0] + ".log")
print("Write the %s log file" % log_filename)
logger = logging.getLogger(__name__)
hdlr_1 = logging.FileHandler(log_filename)
hdlr_1.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(hdlr_1)
logger.setLevel(logging.INFO)


def find_similar(tfidf_matrix, index, top_n=5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index + 1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]


def save_idf_dict(collection, stopwords, filename, stem=False):
    dict_idf = idf_all(collection, stopwords, stem)
    with open("{}.json".format(filename), "w") as f:
        json.dump(dict_idf, f)


def get_idf_dict(filename):
    with open(filename) as f:
        try:
            data = json.load(f)
        except ValueError:
            # if it isn't a correct json, print to log and go on
            raise Exception
        return data


if __name__ == "__main__":
    # sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", "--first", help="", required=True)
    parser.add_argument("-i", "--filename", help="", required=True)
    parser.add_argument("-s", "--stemming", help="", default=False)

    args = parser.parse_args()

    with open(args.first) as f:
        documents_a = json.load(f)


    # cont_a = Counter(doc_a.split())
    # cont_b = Counter(doc_b.split())

    stop_words = set(stopwords.words('italian'))
    # remove it if you need punctuation
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', "«", "»", "’"])

    try:
        doc_a = [
            textblob.TextBlob(doc["_source"]["lyrics"]).lower().replace(".", " ").replace("…", " ").replace("'", " ")
            for doc in documents_a if doc["_source"]["lyrics"]]
    except:
        raise Exception

    save_idf_dict(doc_a, stop_words, args.filename, args.stemming)
