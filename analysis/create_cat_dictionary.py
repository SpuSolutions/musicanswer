import csv
import json

cat_words = dict()
with open("data/item_model.txt") as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        term = row[1].rsplit("-")[0]
        cat = row[0]
        score  = row[2]
        if term not in cat_words:
            cat_words[term] = {cat:score}
        else:
            cat_words[term].update({cat:score})

with open("category_words.json", "w") as f:
    json.dump(cat_words, f)