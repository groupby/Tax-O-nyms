from textblob.classifiers import NaiveBayesClassifier
import json
import time

count = 0
with open("/home/amir/Downloads/parsed2.json") as f:
    train = []
    for line in f:
        j = json.loads(line)
        query = j['query']
        category = j['category']
        count = count + 1
        a = (query, category)
        train.append(a)
        if count >= 1000:
            print "breaking"
            break
    print "traning"
    start_time = time.time()

    cl = NaiveBayesClassifier(train)
    print("--- %s seconds ---" % (time.time() - start_time))

    print "done traning"
    prob_dist = cl.prob_classify("beer")
    print prob_dist.max()
    prob_dist = cl.prob_classify("head phones")
    print prob_dist.max()

    while True:
        print "Enter a query"
        query = raw_input()
        print cl.classify(query)

print "done"

# cl = NaiveBayesClassifier(train)

