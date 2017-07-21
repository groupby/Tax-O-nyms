import json
import sys

import gensim

TOTAL_CATS = 9


def loadCat():
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

    return cat


def printOutput(vectors, category):
    cat = loadCat()
    position = cat.get(category)
    for vector in vectors:
        sys.stdout.write(str(vector) + " ")
    for i in range(0, TOTAL_CATS):
        if position == i:
            sys.stdout.write('1')
        else:
            sys.stdout.write('0')
        if i != TOTAL_CATS - 1:
            sys.stdout.write(' ')

    sys.stdout.write('\n')


# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('/home/amir/dev/GoogleNews-vectors-negative300.bin', binary=True)
failedCount = 0
categories = loadCat()
with open("/home/amir/Downloads/parsedTotal.json") as f:
    for line in f:
        try:
            j = json.loads(line)
            query = j['query']
            category = j['category']
            if query:
                tokens = query.split()
                if (len(tokens)) == 1:
                    for token in tokens:
                        try:
                            vector = model[token]
                            printOutput(vector, category)
                        except KeyError:
                            failedCount += 1
                            pass
        except ValueError:
            pass
