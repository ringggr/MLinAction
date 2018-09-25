from math import log

def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	lableCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in lableCounts.keys():
			lableCounts[currentLabel] = 0
		lableCounts[currentLabel] += 1
	shannonEnt = 0.0
	for key in lableCounts:
		prob = float(lableCounts[key]) / numEntries
		shannonEnt -= prob * log(prob, 2)
	return shannonEnt


def createDataSet():
	dataSet = [[1, 1, 'yes'],
				[1, 1, 'yes'],
				[1, 0, 'no'],
				[0, 1, 'no'],
				[0, 1, 'no']]
	labels = ['no surfacing', 'flippers']
	return dataSet, labels


# Divide data sets by given characteristics
def splitDataSet(dataSet, axis, value):
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis + 1])
			retDataSet.append(reducedFeatVec)
	return retDataSe