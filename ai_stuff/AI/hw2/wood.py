# Connor Wood
# python wood.py 10 hw2_training.txt hw2_testing.txt
# python wood.py k trainData testData

from __future__ import division
import sys
import math
import numpy as np
from random import randint
from sets import Set

THRESHOLD = 1
CLASSES = []

def classCount(trainData):
	for data in trainData:
		if data[3] not in CLASSES:
			CLASSES.append(data[3])
	CLASSES.sort()

def computeTable(k, vectors, trainData):
	table=[]
	classes = []
	count = []
	for data in trainData:
		if data[3] in classes:
			count[classes.index(data[3])] +=1
		else:
			classes.append(data[3])
			count.append(1)

	for v in vectors:
		for c in CLASSES:
			tempcount = 0
			for data in trainData:
				if data[0] == v[0] and data[3] == c:
					tempcount += 1
			table.append([v[0],c,tempcount/count[classes.index(c)]])

	for row in classes:
		table.append([str(row), str(count[classes.index(row)]/len(trainData))])

	for row in table:
		if len(row) == 3:
			print 'P(V=' + row[0] + '|C=' + row[1] +')=' + str(row[2])
		if len(row) == 2:
			print 'P(C=' + row[0] + ')=' + row[1]

	return table

def updateMeanOfVectors(vectors, trainData):
	for v in vectors:
		meanX = 0
		meanY = 0
		count = 0
		for data in trainData:
			if (data[0] == v[0]):
				count += 1
				meanX += float(data[1])
				meanY += float(data[2])
	
		if count < THRESHOLD:
			num = randint(0,len(trainData)-1)
			v[1] = trainData[num][1]
			v[2] = trainData[num][2]
		else:	
			v[1] = meanX/count
			v[2] = meanY/count


def closestVector(vectors, data):
	dist = sys.maxint
	vector = None

	for v in vectors:
		distTemp = math.hypot(float(v[1]) - float(data[1]), float(v[2]) - float(data[2]))
		if distTemp < dist:
			dist = distTemp
			vector = v[0]
	return vector

def train(vectors, trainData):
	converaged = False

	while not converaged:
		converaged = True
		for data in trainData:
			tempData = closestVector(vectors, data) 
			if data[0] != tempData:
				converaged = False
			data[0] = tempData
		updateMeanOfVectors(vectors, trainData)

def test(vectors, testData, table):
	alpha = 0
	for data in testData:
		v = closestVector(vectors, data)

		#alpha
		for row in table:
			if len(row)==3 and row[0]==v:
				for row2 in table:
					if len(row2) ==2 and row2[0] ==row[1]:
						alpha += float(row[2])*float(row2[1])

		#compute class 
		prob = 0
		condProb = 0
		classProb = 0
		classGuess = None
		for c in CLASSES:
			for info in table:
				if len(info)==3 and info[0] == v and info[1]==c:
					condProb = info[2]
				if len(info)==2 and info[0] == c:
					classProb = info[1]
			probTemp = (float(condProb) * float(classProb)) / alpha
			#print probTemp
			if probTemp > prob:
				prob = probTemp
				classGuess = c
		data.append(classGuess)

def errorRate(testData):
	errors = 0
	for data in testData:
		if data[0] != data[3]:
			errors += 1
	return errors/len(testData)


if __name__ == "__main__":
	errors = []
	for iteration in range(10):
		vectors = []
		trainData = []
		testData = []

		for line in open(sys.argv[2]):
			line = line.strip()
			values = line.split('\t')
			values.append(values[0])
			# new temp group number, x, y, given actual class number
			trainData.append(values)

		for i in range(int(sys.argv[1])):
			# i temp group number, x, y
			num = randint(0,len(trainData)-1)
			vectors.append(np.array([i, trainData[num][1],trainData[num][2]]))

		for line in open(sys.argv[3]):
			line = line.strip()
			values = line.split('\t')
			# given actual class number, x, y, (future: guess)
			testData.append(values)

		classCount(trainData)

		train(vectors, trainData)

		table = computeTable(sys.argv[1], vectors, trainData)

		test(vectors, testData, table)

		errors.append(errorRate(testData))

	print 'Classification Error Rate Mean: ' +str(np.mean(errors)) + ' STD: ' + str(np.std(errors))	



