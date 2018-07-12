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
stop_words.update(["essere", "poi", "quando", "altro", "solo", "avere"])
years = [i for i in range(1950, 2020, 10)]
total_most_common = dict()
counter_all = Counter()
total_songs = dict()
excluded = ["disgusto", "attese"]
for year in years:
    most_common = dict()
    path = os.path.join(PAGES_DIR, str(year) + "all")
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
                    if row[2] in cat_data and pos == pos_analysis:
                        lemma_list.add(lemma)
                        if cat_data[lemma] not in excluded:
                            appo = removekey(cat_data[lemma], "attese")
                            data_cat = removekey(appo, "disgusto")
                            most_common[lemma] = data_cat
            c.update(lemma_list)
    # update the term count in
    total_songs[year] = num_songs
    print(num_songs)
    for w in c:
        most_common[w]["count"] = c[w]

    with open("data/most_common_lemma{}.json".format(year), "w") as f:
        json.dump(most_common, f)

    with open('data/most_common{}.csv'.format(year), 'w') as f:
        w = csv.writer(f)
        w.writerow(["id", "value", "emotion"])
        for term in most_common:
            if most_common[term]["count"] >= 10:
                stats = removekey(most_common[term], "count")
                max_key = max(stats.items(), key=operator.itemgetter(1))[0]
                row = (term, most_common[term]["count"], max_key)
                w.writerow(row)
    counter_all.update(c)
    total_most_common[year] = c.most_common(20)

print(total_songs)
the_best = counter_all.most_common(10)
the_best = dict((x, y) for x, y in the_best)
cont = dict()
rows = []
total_songs_value = sum(total_songs.values())
with open('data/most_common_all_{}.csv'.format(pos_analysis), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target", "value"])

    for year in total_most_common:
        word_counter = total_most_common[year]
        for tuple_w in word_counter:
            term = tuple_w[0]
            count = tuple_w[1]
            if term in the_best:
                if term not in cont:
                    cont[term] = {year: count}
                else:
                    cont[term].update({year: count})
    years_words = dict()
    for w in cont:
        index = 0
        for year in cont[w]:
            weight = cont[w][year]
            row = [w, year, weight / float(count_songs[index]) * 100]
            rows.append(row)
            index += 1

    sorted(rows, key=_itemgetter(1))
    for r in rows:
        writer.writerow(r)
