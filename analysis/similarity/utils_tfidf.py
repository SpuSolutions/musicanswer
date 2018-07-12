# http://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/

# https://textblob.readthedocs.io/en/latest/
from utils_tfidf import *
import math
from collections import Counter
from nltk.stem.snowball import SnowballStemmer


def cosine_tf(tokens_a, tokens_b, stopwords=[], dict_idf=None):
    "Anna elisabella Anna"
    occ_a = Counter(tokens_a.split())
    occ_b = Counter(tokens_b.split())
    intersection = set(occ_a.keys()) & set(occ_b.keys())
    if not dict_idf:
        dict_idf = dict()
        dict_idf = {word: 1 for word in set(occ_a.keys()) | set(occ_b.keys())}
    else:
        for word in set(occ_a.keys()) | set(occ_b.keys()):
            dict_idf[word] = dict_idf[word] if word in dict_idf else 0

    # num = sum(occ__a[t] / float(len(tokensA)) * occ_b[t] / float(len(tokensB)) for t in intersection)
    num = sum(
        occ_a[t] / float(len(tokens_a)) * dict_idf[t] * occ_b[t] / float(len(tokens_b)) * dict_idf[t] for t in
        intersection if t not in stopwords)
    # NB: possiamo usare IDF: indice di rarita' del termine, quindi molto piu' indicativo nel ns caso.
    # Dara' piu' peso alle entita' che sono specifiche e che si ripetono nei doc confrontati.
    # Calcolare idf (counter di doc in cui appare il singolo termine) e moltiplicarlo a occ__a[t]/float(len(tokensA)) (e occ_b) ogni volta che appare.

    sum1 = sum([(occ_a[x] / float(len(tokens_a)) * dict_idf[x]) ** 2 for x in occ_a if x not in stopwords])
    sum2 = sum([(occ_b[x] / float(len(tokens_b)) * dict_idf[x]) ** 2 for x in occ_b if x not in stopwords])
    # MODIFICA: [...for x in tokensA] e [...tokensB] al posto di intersection (altrimenti valore risulta piu' elevato)
    # MODIFICA: occ__a[x] diviso su len(tokensA)
    den = math.sqrt(sum1) * math.sqrt(sum2)

    return num / den


def get_tb_cosine(a, b, mode="tf"):
    intersection = set(a.words) & set(b.words)

    if not mode:
        numerator = sum(tf(t, a) * tf(t, b) for t in intersection)
        sum1 = sum((tf(t, a)) ** 2 for t in a.words)
        sum2 = sum((tf(t, b)) ** 2 for t in b.words)
        # denominatore non su intersezione ma su intero doc 
    elif mode == "tf":
        numerator = sum(tf(t, a) / float(len(a)) * tf(t, b) / float(len(b)) for t in intersection)
        sum1 = sum((tf(t, a) / float(len(a))) ** 2 for t in a.words)
        sum2 = sum((tf(t, b) / float(len(b))) ** 2 for t in b.words)
    elif mode == "idf":
        numerator = sum(tfidf(t, a, [a, b]) * tfidf(t, b, [a, b]) for t in intersection)
        sum1 = sum(tfidf(t, a, [a, b]) ** 2 for t in a.words)
        sum2 = sum(tfidf(t, b, [a, b]) ** 2 for t in b.words)
    else:
        numerator = sum1 = sum2 = 0

    # tfidf
    # sum1 = sum(tf(t, a)*idf(t,[a,b]) ** 2 for t in intersection)

    # tf pura
    # sum1 = sum(tf(t, a) ** 2 for t in intersection)

    # tf diviso la lunghezza del documento
    # sum1 = sum(tf(t, a)/ float(len(a))) ** 2 for t in intersection)
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = text.split()
    return Counter(words)


def idf_all(collection, stopwords=[], stem=False):
    c = Counter()
    stemmer = SnowballStemmer("italian")
    for doc in collection:
        if stem:
            terms = set(stemmer.stem(w) for w in doc.words if w not in stopwords)
        else:
            terms = set(w for w in doc.words if w not in stopwords)
        for t in terms:
            c[t] += 1
    return {word: math.log(len(collection) / c[word]) for word in c}


## Other example
# pero' questo non e' normalizzato rispetto alla lunghezza del documento
def get_cosine_method(tokens_a, tokens_b):
    # count word occurrences
    a_vals = Counter(tokens_a)  # word_counts per textblob
    b_vals = Counter(tokens_b)

    # convert to word-vectors
    words = list(a_vals.keys() | b_vals.keys())
    a_vect = [a_vals.get(word, 0) for word in words]  # [0, 0, 1, 1, 2, 1]
    b_vect = [b_vals.get(word, 0) for word in words]  # [1, 1, 1, 0, 1, 0]

    # find cosine
    len_a = sum(av * av for av in a_vect) ** 0.5  # sqrt(7)
    len_b = sum(bv * bv for bv in b_vect) ** 0.5  # sqrt(4)
    dot = sum(av * bv for av, bv in zip(a_vect, b_vect))  # 3
    cosine = dot / (len_a * len_b)
    return cosine


def square_rooted(x):
    return round(math.sqrt(sum([a * a for a in x])), 3)


def cos_similarity(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return round(numerator / float(denominator), 3)
