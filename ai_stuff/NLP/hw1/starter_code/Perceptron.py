from __future__ import division
import sys
import numpy as np
from Eval import Eval
import math
from imdb import IMDBdata
from scipy.sparse import csr_matrix

#Connor Wood
# python Perceptron.py ../data/aclImdb 10
# python Perceptron.py dataFile iterations

class Perceptron:
    def __init__(self, X, Y, N_ITERATIONS):
        self.N_ITERATIONS = N_ITERATIONS
        weightstemp = [0 for i in range(X.get_shape()[1])]
        self.weights = csr_matrix((weightstemp, ([0 for i in range(len(weightstemp))], [i for i in range(len(weightstemp))])))
        self.bias = 0

        self.u = csr_matrix((weightstemp, ([0 for i in range(len(weightstemp))], [i for i in range(len(weightstemp))])))
        self.b = 0
        self.c = 1

        self.Train(X,Y)

    def ComputeAverageParameters(self):
        self.weights -= self.u.multiply(1/self.c)
        self.bias -= (1/self.c)*self.b

    def Train(self, X, Y):
        print "training..."
        iterations = X.get_shape()[0]

        for iteration in range(self.N_ITERATIONS):
            for document in range(iterations):
                row = X.getrow(document)
                a = (row.dot(self.weights.transpose())).max() + self.bias

                if ((Y[document] * a) <= 0):
                    self.weights += row.multiply(Y[document])
                    self.bias += Y[document]
                    self.u += row.multiply(Y[document]*self.c)
                    self.b += Y[document]*self.c
                self.c += 1
            print str(iteration+1) +'/' + str(self.N_ITERATIONS)
        return

    def Predict(self, X):
        pred = []
        a = 0

        for document in range(X.get_shape()[0]):
            a = (X.getrow(document).dot(self.weights.transpose())).toarray()[0][0] + self.bias
            pred.append(1 if a >=0 else -1)

        return pred

    def Eval(self, X_test, Y_test):
        print "testing..."
        Y_pred = self.Predict(X_test)
        ev = Eval(Y_pred, Y_test)
        return ev.Accuracy()

if __name__ == "__main__":
    train = IMDBdata("%s/train" % sys.argv[1])
    test  = IMDBdata("%s/test" % sys.argv[1], vocab=train.vocab)
    
    ptron = Perceptron(train.X, train.Y, int(sys.argv[2]))
    print "non average:"
    print ptron.Eval(test.X, test.Y)
    print "average:"
    ptron.ComputeAverageParameters()
    print ptron.Eval(test.X, test.Y)

    #Print out the 20 most positive and 20 most negative words
    weights = ptron.weights.toarray()[0]
    weightsIDS = []
    for i in range(len(weights)):
        weightsIDS.append([weights[i],i])

    weightsIDS.sort()
    weightsNeg = weightsIDS[:20]
    weightsPos = weightsIDS[len(weightsIDS)-20:]
    for id in weightsNeg:
        print str(id[0]) + " " + train.vocab.GetWord(id[1])
    for id in weightsPos:
        print str(id[0]) + " " + train.vocab.GetWord(id[1])














