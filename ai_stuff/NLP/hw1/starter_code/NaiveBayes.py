from __future__ import division
import sys
import numpy as np
from Eval import Eval
import math
from imdb import IMDBdata
from scipy.sparse import csr_matrix

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

        negs = csr_matrix(1*(traindata.Y<0))
        pos = csr_matrix(1*(traindata.Y>0))
        self.negDocs = negs.get_shape()[1]
        self.posDocs = pos.get_shape()[1]
        self.posWordCount = pos * X
        self.negWordCount = negs * X
        self.posWordCountSum = self.posWordCount.sum()
        self.negWordCountSum = self.negWordCount.sum()

        return

    # this returns prob(Class = 1 | words), where words is a single document
    def PredictProbSingle(self, words):
        # P(class = 1) and P(class = -1)
        PP = self.posDocs / (self.posDocs+self.negDocs)
        PN = self.negDocs / (self.posDocs+self.negDocs)
        posWordCount = self.posWordCount.toarray()[0]
        negWordCount = self.negWordCount.toarray()[0]
        docA = words.toarray()[0]
        
        prob = 1
        PWgivenP = 1
        PWgivenN = 1
     
        #compute P(x1...xn | class = 1) and P(x1...xn | class = -1) 
        for i in words.nonzero()[1]:
            posNumerator = posWordCount[i] + self.ALPHA
            negNumerator = negWordCount[i] + self.ALPHA
            PWgivenP +=  docA[i] * math.log(posNumerator / (self.posWordCountSum + (self.ALPHA * words.get_shape()[1])))
            PWgivenN +=  docA[i] * math.log(negNumerator / (self.negWordCountSum + (self.ALPHA * words.get_shape()[1])))

        #normalize
        prob =(PWgivenP + math.log(PP)) - self.LogSum(PWgivenN+math.log(PN), PWgivenP+math.log(PP) ) 

        return math.exp(prob)

    def PredictLabel(self, X):
        Y = [None] * X.get_shape()[0]
        count = 0
        posWordCount = self.posWordCount.toarray()[0]
        negWordCount = self.negWordCount.toarray()[0]

        i1 = 0
        PP = self.posDocs / (self.posDocs+self.negDocs)
        PN = self.negDocs / (self.posDocs+self.negDocs)
        for doc in X:
            docA = doc.toarray()[0]
            
            prob = 1
            PWgivenP = 1
            PWgivenN = 1

            #compute P(x1...xn | class = 1) and P(x1...xn | class = -1) 
            for i in doc.nonzero()[1]:
                posNumerator = posWordCount[i] + self.ALPHA
                negNumerator = negWordCount[i] + self.ALPHA
                PWgivenP +=  docA[i] * math.log(posNumerator / (self.posWordCountSum + (self.ALPHA * doc.get_shape()[1])))
                PWgivenN +=  docA[i] * math.log(negNumerator / (self.negWordCountSum + (self.ALPHA * doc.get_shape()[1])))

            if (PWgivenN+math.log(PN)> PWgivenP+math.log(PP)):
                Y[count] = -1.0
            else:
                Y[count] = 1.0
            count += 1

        return Y

    def LogSum(self, logx, logy):   
        maxP = max(logx, logy)
        return (maxP + math.log(math.exp(logx - maxP) + math.exp(logy-maxP)))

    def PredictProb(self, test, indexes):
    
        for i in indexes:
            predicted_prob = self.PredictProbSingle(test.X.getrow(i))
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
