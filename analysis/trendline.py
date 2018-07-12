import json
import csv
import os
from nltk.corpus import stopwords


def listdir_nohidden(path, suffix):
    for f in os.listdir(path):
        if not f.startswith('.') and f.endswith(suffix):
            yield f


num_songs = [299, 601, 552, 521, 981, 969, 525]
total_songs = sum(num_songs)
path = "data"
years = [i for i in range(1950, 2020, 10)]
rows = []
total_words = 0
index = 0
stop_words = set(stopwords.words('italian'))
stop_words.update(["essere", "poi", "quando", "altro", "solo"])

for year in years:
    with open(os.path.join(path, "most_common_lemma{}.json".format(year))) as f:
        data = json.load(f)
    scoreJoy = scoreSad = scoreAnger = scoreSurp = scoreFear = scoreTrust = 0
    num_words = len(data)
    counted_words = sum(data[w]["count"] for w in data)

    for word in data:
        if word not in stop_words:
            count = data[word]["count"]
            scoreJoy += count * float(data[word]["gioia"])
            scoreSad += count * float(data[word]["tristezza"])
            scoreAnger += count * float(data[word]["rabbia"])
            scoreSurp += count * float(data[word]["sorpresa"])
            scoreFear += count * float(data[word]["paura"])
            scoreTrust += count * float(data[word]["fiducia"])

    normalize = 1 / float(sum([scoreJoy, scoreSad, scoreAnger, scoreSurp, scoreFear, scoreTrust])) * 100

    rows.append([year, scoreJoy * normalize, scoreSad * normalize, scoreAnger * normalize, scoreSurp * normalize,
                 scoreFear * normalize, scoreTrust * normalize])
    index += 1
with open(os.path.join(path, "trendline.csv"), "w") as csvfile:
    writer = csv.writer(csvfile, delimiter="\t")
    writer.writerow(["date", "gioia", "tristezza", "rabbia", "sorpresa", "paura", "fiducia"])
    for row in rows:
        writer.writerow(row)
