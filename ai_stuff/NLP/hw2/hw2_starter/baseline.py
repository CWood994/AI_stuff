#Connor Wood
#python baseline.py data/twitter_train_universal.txt data/twitter_test_universal.txt 

from __future__ import division
import sys
import math
import numpy as np

def most_common(lst):
    return max(set(lst), key=lst.count)

def train(data):
    dataDict = {}

    for d in data:
        if d[0] in dataDict:
            dataDict[d[0]].append(d[1])
        else:
            dataDict[d[0]] = [d[1]]

    return dataDict


def orderData(dataDict, testData):
    results = []

    for word in testData:
        if word in dataDict:
            results.append([word, most_common(dataDict[word])])
        else:
            results.append([word, "NOUN"])

    return results

if __name__ == "__main__":
    trainData = []
    testData = []

    for line in open(sys.argv[1]):
        fields = line.strip().split()
        if len(fields) == 2:
            trainData.append(fields)

    for line in open(sys.argv[2]):
        fields = line.strip().split()
        if len(fields) == 2:    
            testData.append(fields[0])

    dataDict = train(trainData)
    results = orderData(dataDict, testData)

    with open("mft_baseline.out", "w") as text_file:
        for result in results:
            text_file.write(str(result[0]) + " " + str(result[1]) + "\n")