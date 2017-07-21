import json
import sys

import gensim

TOTAL_CATS = 9
cat = {
    "baby & child": 0,
    "beauty": 1,
    "diet & nutrition": 2,
    "health & medicine": 3,
    "home health care": 4,
    "household & grocery": 5,
    "personal care": 6,
    "sexual health": 7,
    "vitamins": 8
}


def printCatVec(categories):
    count = 0
    for key in cat:
        matched = False
        for category in categories:
            if category[u"value"] == key:
                sys.stdout.write(str(category[u"percentage"]))
                matched = True
        if not matched:
            sys.stdout.write('0')
        if count != TOTAL_CATS - 1:
            sys.stdout.write(' ')
        count += 1
    print


def printOutput(vectors, category):
    for vector in vectors:
        sys.stdout.write(str(vector) + " ")
    printCatVec(category)


# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('/home/amir/dev/GoogleNews-vectors-negative300.bin', binary=True)


def main():
    with open("../outputMultiCat") as f:
        try:
            for line in f:
                j = json.loads(str(line), "utf-8")
                query = j['query']
                category = j['category']
                if query:
                    tokens = query.split()
                    for token in tokens:
                        try:
                            vector = model[token]
                            printOutput(vector, category)
                        except KeyError, e:
                            print e
                            pass
        except ValueError, e:
            print e
            pass
        except KeyError, e:
            print e
            pass


main()
