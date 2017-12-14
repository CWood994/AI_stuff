# Connor Wood
# python wood2.py 10 hw2_training.txt hw2_testing.txt 2
# python wood2.py k trainData testData dimensions

from __future__ import division
import sys
import math
import numpy as np
from random import randint
from sets import Set

THRESHOLD = 1
CLASSES = []
N = 2

def classCount(trainData):
	for data in trainData:
		if data[N+1] not in CLASSES:
			CLASSES.append(data[N+1])
	CLASSES.sort()

def computeTable(k, vectors, trainData):
	table=[]
	classes = []
	count = []
	for data in trainData:
		if data[N+1] in classes:
			count[classes.index(data[N+1])] +=1
		else:
			classes.append(data[N+1])
			count.append(1)

	for v in vectors:
		for c in CLASSES:
			tempcount = 0
			for data in trainData:
				if data[0] == v[0] and data[N+1] == c:
					tempcount += 1
			table.append([v[0],c,tempcount/count[classes.index(c)]])

	for row in classes:
		table.append([str(row), str(count[classes.index(row)]/len(trainData))])

	#print vectors
	#for row in table:
	#	if len(row) == 3:
	#		print 'P(V=' + row[0] + '|C=' + row[1] +')=' + str(row[2])
	#	if len(row) == 2:
	#		print 'P(C=' + row[0] + ')=' + row[1]

	return table

def updateMeanOfVectors(vectors, trainData):
	for v in vectors:
		means = [0 for i in range(N)]
		count = 0
		for data in trainData:
			if (data[0] == v[0]):
				count += 1
				for i2 in range(N):
					means[i2] += float(data[i2+1])
	
		if count < THRESHOLD:
			num = randint(0,len(trainData)-1)
			for i3 in range(N):
				v[i3+1] = trainData[num][i3+1]

		else:	
			for i4 in range(N):
				v[i4+1] = means[i4]/count


def closestVector(vectors, data):
	dist = sys.maxint
	vector = None

	for v in vectors:
		p1 = np.array([])
		p2 = np.array([])	

		for i in range(N):
			p1 = np.append(p1, float(v[i+1]))
			p2 = np.append(p2, float(data[i+1]))

		distTemp = np.linalg.norm(p1-p2)

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
			probTemp = (float(condProb) * float(classProb)) 
			#print probTemp
			if probTemp > prob:
				prob = probTemp
				classGuess = c
		data.append(classGuess)

def errorRate(testData):
	errors = 0
	for data in testData:
		if data[0] != data[N+1]:
			errors += 1
	return errors/len(testData)


if __name__ == "__main__":
	errors = []
	N = int(sys.argv[4])

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
			vectors.append(np.append(np.array([i]), trainData[num][1:int(N)+1]))

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



