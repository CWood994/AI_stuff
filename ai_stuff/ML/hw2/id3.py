from __future__ import division
from collections import namedtuple
import sys
import math
from Data import *

DtNode = namedtuple("DtNode", "fVal, nPosNeg, gain, left, right")

POS_CLASS = 'e'

def InformationGain(data, f):
    #TODO: compute information gain of this dataset after splitting on feature F

    t_count = nPosCalc(data)
    p_before = t_count/len(data)
    if p_before ==0 or p_before==1:
        return 0
    entropy_before = - ((p_before * math.log(p_before,2.0)) + ((1-p_before) * math.log((1-p_before),2.0)))

    t_data = dataSet(data, f, True)
    t_data_count = nPosCalc(t_data)
    f_data = dataSet(data, f, False)
    f_data_count = nPosCalc(f_data)
    if len(t_data) ==0 or len(t_data)==len(data):
        return 0

    p_t_data = t_data_count / len(t_data)
    if p_t_data == 0 or p_t_data==1:
        et = 0
    else:
        et = -((p_t_data * math.log(p_t_data,2.0)) + ( (1 - p_t_data) * math.log(1 - p_t_data,2.0)))
        et *= (len(t_data)/len(data)) 

    
    p_f_data = f_data_count / len(f_data)
    if p_f_data == 0 or p_f_data==1:
        ef = 0
    else:
        ef = -((p_f_data * math.log(p_f_data,2.0)) + ( (1 - p_f_data) * math.log(1 - p_f_data,2.0)))
        ef *= (len(f_data)/len(data)) 

    return entropy_before - (et+ef)

def Classify(tree, instance):
    if tree.left == None and tree.right == None:
        return tree.nPosNeg[0] > tree.nPosNeg[1]
    elif instance[tree.fVal.feature] == tree.fVal.value:
        return Classify(tree.left, instance)
    else:
        return Classify(tree.right, instance)

def Accuracy(tree, data):
    nCorrect = 0
    for d in data:
        if Classify(tree, d) == (d[0] == POS_CLASS):
            nCorrect += 1
    return float(nCorrect) / len(data)

def PrintTree(node, prefix=''):
    print("%s>%s\t%s\t%s" % (prefix, node.fVal, node.nPosNeg, node.gain))
    if node.left != None:
        PrintTree(node.left, prefix + '-')
    if node.right != None:
        PrintTree(node.right, prefix + '-')        

def nPosCalc(data):
    f_count = 0

    for shroom in data:
        if shroom[0]==POS_CLASS:
            f_count += 1

    return f_count

def dataSet(data, f, condition):
    mySet = []

    for shroom in data:
        if (shroom[f[0]]==f[1]) == condition :
            mySet.append(shroom)

    return mySet

       
def ID3(data, features, MIN_GAIN=0.5):
    #TODO: implement decision tree learning

    max_entrophy = 0
    feature = None
    for f in features:
        temp_entrophy = InformationGain(data, f)
        if(temp_entrophy > max_entrophy):
            feature = f
            max_entrophy = temp_entrophy

    if(max_entrophy<MIN_GAIN or feature==None):
        return DtNode(feature, (nPosCalc(data),len(data)-nPosCalc(data)), max_entrophy, None, None)

    features.remove(feature)
    return DtNode(feature, (nPosCalc(data),len(data)-nPosCalc(data)), max_entrophy, ID3(dataSet(data,feature,True), features, MIN_GAIN), ID3(dataSet(data,feature,False), features, MIN_GAIN))

if __name__ == "__main__":
    train = MushroomData(sys.argv[1])
    dev = MushroomData(sys.argv[2])

    dTree = ID3(train.data, train.features, MIN_GAIN=float(sys.argv[3]))
    
    PrintTree(dTree)

    print Accuracy(dTree, dev.data)
