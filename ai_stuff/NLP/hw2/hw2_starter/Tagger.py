import sys

import numpy as np

from scipy.sparse import csr_matrix
from Data import LinearChainData

class Tagger(object):
    def __init__(self, average=True):
        self.useAveraging = average

    def ComputeThetaAverage(self):
        temp = self.u/self.c
        self.thetaAverage = self.theta - temp

    def PrintableSequence(self, sequence):
        return [self.train.tagVocab.GetWord(x) for x in sequence]

    def DumpParameters(self, outFile):
        fOut = open(outFile, 'w')
        sortedParams = (np.argsort(self.thetaAverage, axis=None)[::-1])[0:500]
        for i in sortedParams:
            (tag1ID, tag2ID, featureID) = np.unravel_index(i, self.theta.shape)
            fOut.write("%s %s %s %s\n" % (self.train.tagVocab.GetWord(tag1ID), self.train.tagVocab.GetWord(tag2ID), self.train.vocab.GetWord(featureID), self.thetaAverage[tag1ID,tag2ID,featureID]))
        fOut.close()
    
    def Train(self, nIter):
        self.c = 1
        self.u = np.copy(self.theta)
        for i in range(nIter):
            nSent = 0
            for (s,g) in self.train.featurizedSentences:
                if len(g) <= 1:         #Skip any length 1 sentences - some numerical issues...
                    continue
                z = self.Viterbi(s, self.theta, len(g))

                sys.stderr.write("Iteration %s, sentence %s\n" % (i, nSent))
                sys.stderr.write("predicted:\t%s\ngold:\t\t%s\n" % (self.PrintableSequence(z), self.PrintableSequence(g)))
                nSent += 1
                if z != g.tolist():
                    self.UpdateTheta(s,g,z, self.theta, len(g), self.c, self.u)
                self.c += 1

        if self.useAveraging:
            self.ComputeThetaAverage()
    

class ViterbiTagger(Tagger):
    def __init__(self, inFile, average=True):
        self.train = LinearChainData(inFile)
        self.useAveraging = average

        self.ntags    = self.train.tagVocab.GetVocabSize()
        self.theta    = np.zeros((self.ntags, self.ntags, self.train.vocab.GetVocabSize()))   #T^2 parameter vectors (arc-emission CRF)
        self.thetaSum = np.zeros((self.ntags, self.ntags, self.train.vocab.GetVocabSize()))   #T^2 parameter vectors (arc-emission CRF)
        self.nUpdates = 0

    def TagFile(self, testFile):
        self.test = LinearChainData(testFile, vocab=self.train.vocab)
        for i in range(len(self.test.sentences)):
            featurizedSentence = self.test.featurizedSentences[i][0]
            sentence = self.test.sentences[i]
            if self.useAveraging:
                v = self.Viterbi(featurizedSentence, self.thetaAverage, len(sentence))
            else:
                v = self.Viterbi(featurizedSentence, self.theta, len(sentence))
            words = [x[0] for x in sentence]
            tags  = self.PrintableSequence(v)
            for i in range(len(words)):
                print "%s\t%s" % (words[i], tags[i])
            print ""

    def Viterbi(self, featurizedSentence, theta, slen):
        viterbiSeq = []
        pi = [1 for i in range(self.ntags)]
        backpointers = [[0 for j in range(self.ntags)] for i in range(slen)]

        #calculate pi for first sentence using START as prev tag
        pi_last = []
        for i in range(self.ntags):
            # +1 needed for due to init pi(0,*)=1 ..?
            pi_last.append(featurizedSentence[0].dot(theta[i,0]) + pi[i])

        # for each word
        for k in range(1,slen):

            #find max pi for previous tag and current tag
            #u = current tag
            for u in range(1,self.ntags):
                #v = previous tag          
                pis = [featurizedSentence[k].dot(theta[u,v]) + pi_last[v] for v in range(1,self.ntags)]
                
                #save max pi for cur tag and save tag for backpointer
                backpointers[k][u] = np.argmax(pis)+1
                pi[u] = pis[np.argmax(pis)]

            pi_last = list(pi)

        #assign last tag to max of pi
        viterbiSeq.append(pi.index(max(pi)))

        #work way to start, setting tags
        for k in reversed(range(1,slen)):
            viterbiSeq.append( backpointers[k][viterbiSeq[len(viterbiSeq)-1]] )

        viterbiSeq.reverse()
        return viterbiSeq

 
    #Structured Perceptron update
    def UpdateTheta(self, sentenceFeatures, 
                          goldSequence, 
                          viterbiSequence,
                          theta,
                          slen, c, u):
        
        START_TAG = self.train.tagVocab.GetID('START')


        for i in range(0,slen):
            if goldSequence[i] != viterbiSequence[i]: 
                theta[viterbiSequence[i], viterbiSequence[i-1]] -= sentenceFeatures[i]
                theta[goldSequence[i], goldSequence[i-1]] += sentenceFeatures[i]
                u[viterbiSequence[i], viterbiSequence[i-1]] -= sentenceFeatures[i].multiply(c)
                u[goldSequence[i],  goldSequence[i-1]] += sentenceFeatures[i].multiply(c)

                
