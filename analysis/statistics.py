import os
import argparse
import csv


def listdir_nohidden(path, suffix):
    for f in os.listdir(path):
        if not f.startswith('.') and f.endswith(suffix):
            yield f


parser = argparse.ArgumentParser(description='')
parser.add_argument("-i", "--input", help="Output existing directory, will contain the JSON files", required=True)
args = parser.parse_args()

num_songs = [299, 601, 552, 521, 981, 969, 525]
total_songs = sum(num_songs)
LYRICS_DIR = args.input
years = [i for i in range(1950, 2020, 10)]

all_words = []
all_artists = set()
lemma_list = set()
for year in years:
    path = os.path.join(LYRICS_DIR, str(year) + "all")
    suffix = ".pos"
    list_files = listdir_nohidden(path, suffix)
    for filename in list_files:
        all_artists.add(filename.split("#")[0])
        with open(os.path.join(path, filename), "r") as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) > 1:
                    lemma = row[2]
                    all_words.append(row[1])
                    lemma_list.add(lemma)
print("lemma: {}".format(len(lemma_list)))
print("artisti: {}".format(len(all_artists)))
print("words: {}".format(len(all_words)))
print("set words: {}".format(len(set(all_words))))
