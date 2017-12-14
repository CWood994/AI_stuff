#!/usr/bin/python
# Connor Wood
#########################################################
# CSE 5523 starter code (HW#5)
# Alan Ritter
#########################################################
from __future__ import division
import random
import math
import sys
import re
import matplotlib.pyplot as plt
import numpy as np

#GLOBALS/Constants
VAR_INIT = 1

#The problem is that we don't know the cluster ids for the datapoints.  
#So you need to marginalize out the cluster id (sum the joint probability over all possible cluster assignments) 
#to get the marginal log probability for each data point to add together to get the final log-likelihood. 
# But, there is no log identify for sums - this is one of the two places you will need to use the log-exp-sum trick in the assignment.
def logExpSum(x):
    #TODO: implement logExpSum
    maxX = max(x)
    subtracted = np.array([i-maxX for i in x])
    return maxX + np.log(np.sum(np.exp(subtracted)))

def readTrue(filename='wine-true.data'):
    f = open(filename)
    labels = []
    splitRe = re.compile(r"\s")
    for line in f:
        labels.append(int(splitRe.split(line)[0]))
    return labels

#########################################################################
#Reads and manages data in appropriate format
#########################################################################
class Data:
    def __init__(self, filename):
        self.data = []
        f = open(filename)
        (self.nRows,self.nCols) = [int(x) for x in f.readline().split(" ")]
        for line in f:
            self.data.append([float(x) for x in line.split(" ")])

    #Computes the range of each column (returns a list of min-max tuples)
    def Range(self):
        ranges = []
        for j in range(self.nCols):
            min = self.data[0][j]
            max = self.data[0][j]
            for i in range(1,self.nRows):
                if self.data[i][j] > max:
                    max = self.data[i][j]
                if self.data[i][j] < min:
                    min = self.data[i][j]
            ranges.append((min,max))
        return ranges

    def __getitem__(self,row):
        return self.data[row]

#########################################################################
#Computes EM on a given data set, using the specified number of clusters
#self.parameters is a tuple containing the mean and variance for each gaussian
#########################################################################
class EM:
    def __init__(self, data, nClusters):
        #Initialize parameters randomly...
        random.seed()
        self.parameters = []
        self.priors = []        #Cluster priors
        self.nClusters = nClusters
        self.data = data
        ranges = data.Range()
        for i in range(nClusters):
            p = []
            initRow = random.randint(0,data.nRows-1)
            for j in range(data.nCols):
                #Randomly initalize variance in range of data
                p.append((random.uniform(ranges[j][0], ranges[j][1]), VAR_INIT*(ranges[j][1] - ranges[j][0])))
            self.parameters.append(p)

        #Initialize priors uniformly
        for c in range(nClusters):
            self.priors.append(1/float(nClusters))

    # sum together the log probabilities of each datapoint).
    def LogLikelihood(self, data):
        logLikelihood = 0.0
        #TODO: compute log-likelihood of the data
        for row in range(data.nRows):
            prob_for_each_cluster = []
            for cluster in range(self.nClusters):
                prob_for_each_cluster.append(np.log(self.priors[cluster]) + self.LogProb(row,cluster,data))
            sumed = logExpSum(prob_for_each_cluster)
            logLikelihood += sumed
        return logLikelihood

    #Compute marginal distributions of hidden variables
    # output of E-step is an m*k matrix, by adding along the rows we can get the 1*k matrix that can be used to update the prior.
    def Estep(self):
        #TODO: E-step
        result = []
        for i in range(self.data.nRows):
            clusters = []
            for j in range(self.nClusters):
                clusters.append(self.LogProb(i,j,self.data))
            log_priors = np.log(self.priors)
            clusters_temp = []
            for prior in range(len(log_priors)):
                clusters_temp.append(clusters[prior]+log_priors[prior])
            clusters = clusters_temp
            normalize = logExpSum(clusters)
            result.append(clusters - normalize)
        self.eresults = result
        return np.exp(result)

    #Update the parameter estimates
    def Mstep(self, estep_result):
        #TODO: M-step
        for cluster in range(self.nClusters):
            self.priors[cluster] = np.mean(estep_result[:,cluster])
            for col in range(self.data.nCols):
                x = np.array(self.data.data)[:,col]
                mean = np.sum(estep_result[:,cluster] * x) / np.sum(estep_result[:,cluster])
                sd = np.sqrt(np.sum(estep_result[:,cluster] * np.power(x-mean,2)) / np.sum(estep_result[:,cluster]))
                self.parameters[cluster][col] = (mean, sd)

    # Computes the probability that row was generated by cluster
    # multiply the cluster prior by the conditional probability of each feature given the cluster 
    # log space (e.g. replace probabilities with log-probabilities, and multiplication with sums).
    # http://www.cs.princeton.edu/courses/archive/spr08/cos424/scribe_notes/0214.pdf number 3
    def LogProb(self, row, cluster, data):
        #TODO: compute probability row i was generated by cluster k
        mean = []
        sd = []
        for i in range(data.nCols):
            mean.append(self.parameters[cluster][i][0])
            sd.append(self.parameters[cluster][i][1])
        mean = np.array(mean)

        for tempiforpartd in range(len(sd)):
            if sd[tempiforpartd] == 0:
                sd[tempiforpartd] = .001
        sd = np.array(sd)
        result = (-1/2)*np.log(2*np.pi*np.power(sd,2))
        #print result
        secondPart = np.power((np.array(data.data[row]) - mean),2) / (2* np.power(sd,2))
        #print secondPart
        result = result - secondPart
        #print result.sum()
        return result.sum()

    def Run(self, maxsteps=100, testData=None):
        #TODO: Implement EM algorithm

        train = []
        test = []
        train.append(self.LogLikelihood(self.data))
        test.append(self.LogLikelihood(testData))
        prev = self.LogLikelihood(self.data)
        trainLikelihood = 1
        diff = 1
        step = 0
        first = True
        while first or (diff > .001 and step < maxsteps):
            first = False
            estep_result = self.Estep()
            self.Mstep(estep_result)
            trainLikelihood = self.LogLikelihood(self.data)
            train.append(trainLikelihood)
            test.append(self.LogLikelihood(testData))
            diff = (prev - trainLikelihood)/ prev
            prev = trainLikelihood
            step += 1
        testLikelihood = self.LogLikelihood(testData)

        return (train, test)

if __name__ == "__main__":
    d = Data('wine.train')
    if len(sys.argv) > 1:
        e = EM(d, int(sys.argv[1]))
    else:
        e = EM(d, 3)
    trainLikelihood, testLikelihood = e.Run(100, testData = Data('wine.test'))

    # a
    plt.plot(range(len(trainLikelihood)), trainLikelihood, label = "train", linestyle='--', marker='o')
    plt.plot(range(len(testLikelihood)), testLikelihood, label = "test", linestyle='--', marker='o',)
    plt.ylabel('loglikelihood')
    plt.xlabel('iterations')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


    # b
    train = []
    test = []
    for i in range(10):
        e = EM(d, 3)
        trainLikelihood, testLikelihood = e.Run(100, testData = Data('wine.test'))
        train.append(trainLikelihood[-1])
        test.append(testLikelihood[-1])
    plt.plot(range(len(train)), train, label = "train", linestyle='--', marker='o')
    plt.ylabel('loglikelihood')
    plt.xlabel('iteration')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
    plt.plot(range(len(test)), test, label = "test", linestyle='--', marker='o',)
    plt.ylabel('loglikelihood')
    plt.xlabel('iteration')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
    

    # c
    guesses = [np.argmax(i) + 1 for i in e.eresults]
    gold = readTrue()
    acc_right = []
    acc_wrong = []
    for i in set(guesses):
        indexes = [ind for ind, x in enumerate(guesses) if x == i]
        ind_gold = [x for ind, x in enumerate(gold) if ind in indexes]
        correct = ind_gold.count(max(set(ind_gold), key=ind_gold.count))
        incorrect = len(indexes) - correct
        acc_right.append(correct)
        acc_wrong.append(incorrect)
    print sum(acc_right) / (sum(acc_wrong) + sum(acc_right))
    

    # d
    train = []
    test = []
    for i in range(1,11):
        e = EM(d, i)
        trainLikelihood, testLikelihood = e.Run(100, testData = Data('wine.test'))
        train.append(trainLikelihood[-1])
        test.append(testLikelihood[-1])
    plt.plot(range(len(train)), train, label = "train", linestyle='--', marker='o')
    plt.ylabel('loglikelihood')
    plt.xlabel('# cluster')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
    plt.plot(range(len(test)), test, label = "test", linestyle='--', marker='o',)
    plt.ylabel('loglikelihood')
    plt.xlabel('iteration')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()














