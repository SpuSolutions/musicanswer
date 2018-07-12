import json
import os
import csv
from nltk.corpus import stopwords
from collections import Counter
import operator
from operator import itemgetter as _itemgetter, eq as _eq
import heapq


# we need this for Sankey and bubble chart

def listdir_nohidden(path, suffix):
    for f in os.listdir(path):
        if not f.startswith('.') and f.endswith(suffix):
            yield f


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def most_common(mydict, n=None):
    if n is None:
        return sorted(mydict.items(), key=_itemgetter(1), reverse=True)
    return heapq.nlargest(n, mydict.items(), key=_itemgetter(1))


count_songs = [299, 601, 552, 521, 981, 969, 525]
PAGES_DIR = "data/lemma_lyrics"
cat_words = "data/category_words.json"
pos_analysis = "v"
with open(cat_words, "r") as f:
    cat_data = json.load(f)

stop_words = set(stopwords.words('italian'))
stop_words.update(["essere", "poi", "quando", "altro", "solo", "avere", "etc", "perche", "com", "quant", "tutt", "cap"])
years = [i for i in range(1950, 2020, 10)]
total_most_common = dict()
counter_all = Counter()
total_songs = dict()

for year in years:
    path = os.path.join(PAGES_DIR, str(year) + "all")
    all_words = []
    most_common = dict()
    suffix = ".pos"
    list_files = listdir_nohidden(path, suffix)

    c = Counter()
    num_songs = 0
    for filename in list_files:
        num_songs += 1

        with open(os.path.join(path, filename), "r") as f:
            reader = csv.reader(f, delimiter='\t')
            lemma_list = set()
            for row in reader:
                if len(row) > 1 and row[2] not in stop_words:
                    lemma = row[2]
                    pos = row[3].lower()
                    if row[2] in cat_data:
                        lemma_list.add(lemma)
                        most_common[lemma] = cat_data[lemma]
            all_words.extend(lemma_list)
            c.update(lemma_list)
    print(all_words)
    text = " ".join(all_words)
    print(text)
    with open("data/text{}.txt".format(year), "w") as f:
        f.write(text)

    # update the term count in
    total_songs[year] = num_songs
    print(num_songs)
    for w in c:
        most_common[w]["count"] = c[w]


        