from __future__ import division
import sys
import math

def probOfEdible(trainData):
	edible=0
	for shroom in trainData:
		if shroom[0]=='e':
			edible += 1
	return edible/len(trainData)

def probOfEvidenceForEdible(trainData, intEvidencePos, evidence):
	count = 0
	edible = 0
	for shroom in trainData:
		if shroom[0]=='e':
			edible += 1
			if shroom[intEvidencePos] == evidence:
				count += 1
	return count/edible

def probOfEvidenceForPos(trainData, intEvidencePos, evidence):
	count = 0
	edible = 0
	for shroom in trainData:
		if shroom[0]=='p':
			edible += 1
			if shroom[intEvidencePos] == evidence:
				count += 1
	return count/edible

def probOfEvidenceForAll(trainData, intEvidencePos, evidence):
	count = 0
	for shroom in trainData:
		if shroom[intEvidencePos] == evidence:
			count += 1
	return count/(len(trainData))

def predict(trainData, mushroom):
	result = 1
	alpha = 1
	alphaE = 1
	alphaP=1
	for i in range(1,len(mushroom)):
		result *= probOfEvidenceForEdible(trainData, i, mushroom[i])
		alphaE *= probOfEvidenceForEdible(trainData, i, mushroom[i])
		alphaP *= probOfEvidenceForPos(trainData, i, mushroom[i])

	alpha = ((alphaE*probOfEdible(trainData))+(alphaP*(1-probOfEdible(trainData))))

	result /= alpha
	result *= probOfEdible(trainData)
	return result

if __name__ == "__main__":
	testData = []
	trainData = []
	for line in open(sys.argv[1]):
			line = line.strip()
			values = line.split(',')
			trainData.append(values)
	for line in open(sys.argv[2]):
		line = line.strip()
		values = line.split(',')
		testData.append(values)

	correct = 0
	for shroom in testData:
		value = predict(trainData, shroom)
		print(shroom),
		print('P(e): ' + str(value))
		if value >= .5:
			if shroom[0]=='e':
				correct += 1
		else: 
			if shroom[0]=='p':
				correct+= 1
	print('Accuracy: ' + str(correct/len(testData)))