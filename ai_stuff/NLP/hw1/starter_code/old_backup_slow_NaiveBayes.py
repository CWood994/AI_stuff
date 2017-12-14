from __future__ import division
import sys
import numpy as np
from Eval import Eval
import math
from imdb import IMDBdata

#Connor Wood
# python NaiveBayes.py ../data/aclImdb 10
# python NaiveBayes.py dataFile alpha_hyperParam

class NaiveBayes:
    def __init__(self, data, ALPHA=1.0):
        self.ALPHA = ALPHA
        self.data = data 
        self.Train(data.X,data.Y)

    def Train(self, X, Y):
        print "Training..."
    
        XArray = X.toarray()
        posWordCount = [0 for i in range(len(XArray[0]))]
        negWordCount = [0 for i in range(len(XArray[0]))]
        posDocs = 0
        negDocs = 0

        #count each word in all docs and store according to class
        for i in range(len(XArray)):
            if Y[i] == 1:
                posDocs += 1
                for j in range(len(XArray[i])):
                    posWordCount[j] += XArray[i][j]
            else:
                negDocs += 1
                for j in range(len(XArray[i])):
                    negWordCount[j] += XArray[i][j]


        self.posWordCount = posWordCount
        self.negWordCount = negWordCount
        self.posDocs = posDocs
        self.negDocs = negDocs

        # total count of all words for each class
        self.posWordCountSum = 0
        for i in posWordCount:
            self.posWordCountSum += i

        self.negWordCountSum = 0
        for i in negWordCount:
            self.negWordCountSum += i

        '''
        #For testing purposes to not retrain everytime

        np.savetxt('posWordCount.txt',self.posWordCount,delimiter=',')
        np.savetxt('negWordCount.txt',self.negWordCount,delimiter=',')
        print self.posDocs
        print self.negDocs
        print self.posWordCountSum 
        print self.negWordCountSum


        self.posWordCount = np.loadtxt('posWordCount.txt', delimiter=',').tolist()
        self.negWordCount = np.loadtxt('negWordCount.txt', delimiter=',').tolist()
        self.posDocs = 12500
        self.negDocs = 12500
        self.negWordCountSum = 2885722
        self.posWordCountSum = 2958696
        '''
        return

    # this returns prob(Class = 1 | words), where words is a single document
    def PredictProbSingle(self, words):
        # P(class = 1) and P(class = -1)
        PP = self.posDocs / (self.posDocs+self.negDocs)
        PN = self.negDocs / (self.posDocs+self.negDocs)

        prob = 1
        PWgivenP = 1
        PWgivenN = 1

        #compute P(x1...xn | class = 1) and P(x1...xn | class = -1) 
        for i in range(len(words)):
            if words[i] > 0:
                posNumerator = self.posWordCount[i] + self.ALPHA
                negNumerator = self.negWordCount[i] + self.ALPHA
                PWgivenP +=  words[i] * math.log(posNumerator / (self.posWordCountSum + (self.ALPHA * len(words))))
                PWgivenN +=  words[i] * math.log(negNumerator / (self.negWordCountSum + (self.ALPHA * len(words))))

        #normalize
        prob =(PWgivenP + math.log(PP)) - self.LogSum(PWgivenN+math.log(PN), PWgivenP+math.log(PP) ) 

        return math.exp(prob)

    def PredictLabel(self, X):
        Y = []
        XArray = X.toarray()

        for doc in XArray:
            if (self.PredictProbSingle(doc) >= .5):
                Y.append(+1.0)
            else:
                Y.append(-1.0)
        return Y

    def LogSum(self, logx, logy):   
        maxP = max(logx, logy)
        return (maxP + math.log(math.exp(logx - maxP) + math.exp(logy-maxP)))

    def PredictProb(self, test, indexes):
    
        XArray = test.X.toarray()

        for i in indexes:
            predicted_prob = self.PredictProbSingle(XArray[i])
            predicted_label = 1.0 if (predicted_prob>=.5) else -1.0

            # note: predicted_prob is prob of being positive, thus <.5 will cause predicted_label to be -1
            print test.Y[i], predicted_label, predicted_prob, test.X_reviews[i]


    def Eval(self, test):
        print "testing..."
        Y_pred = self.PredictLabel(test.X)
        ev = Eval(Y_pred, test.Y)
        return ev.Accuracy()


if __name__ == "__main__":

    traindata = IMDBdata("%s/train" % sys.argv[1])
    testdata  = IMDBdata("%s/test" % sys.argv[1], vocab=traindata.vocab)
    
    nb = NaiveBayes(traindata, float(sys.argv[2]))
    print nb.Eval(testdata)
    nb.PredictProb(testdata, range(10)) 
