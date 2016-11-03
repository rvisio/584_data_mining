import numpy as np
import random
from scipy.spatial import distance
import string
import pandas as pd
k = 7

exclude = set(string.punctuation)
centroidDict = {}
def createRandomCentroids(array):
	# get the max and min values, will be used for randomly creating centrodis
	maxValue =5.0
	minValue =5.0
	crcCounter = 0
	for record in X:
		crcCounter += 1
		print 'were now at ' , str(crcCounter)
		for x in record:
			if np.average(x) > maxValue:
				print 'max value was ' , str(maxValue), ' but it is now ' , str(np.average(record))
				maxValue = np.average(x)
			elif np.average(x) < minValue:
				print 'min value was ' , str(minValue), ' but it is now ' , str(np.average(record))
				minValue = np.average(x)

	print 'minValue is now ' , str(minValue)
	print 'maxValue is now ' , str(maxValue)
	# Will need to store them in lists so we can iterate through when calculating averages
	centroidList = []

	for x in range(k):
		print (x)
		centroidList.append((round(random.uniform(minValue, maxValue), 2),round(random.uniform(minValue, maxValue), 2),round(random.uniform(minValue, maxValue), 2),round(random.uniform(minValue, maxValue), 2), round(random.uniform(minValue, maxValue)),round(random.uniform(minValue, maxValue)),round(random.uniform(minValue, maxValue))))
		centroidDict[x] = np.asarray(centroidList)
	print len(centroidList)
	return np.asarray(centroidList)

	# not randomly generating centroids, need to caclulate them based off of the array being passed in



# Create centroids based off the values that are brought in, we will need to
def createCentroids(centroidDictionary):
	print ' creating centroids'
	centroidList = []
	for key, value in centroidDictionary.iteritems():
		print key, value
		centroidDict[key] = (np.average(value))
		centroidList.append(np.average(value))
	print len(centroidList)
	print centroidDictionary
	return centroidList




X = []


# Read data in
with open('../data/features.data') as irisData:
	for line in irisData:
		print ' reading data'
		processDataCount = 0
		line = line.split()
		tempRecord = []
		for x in line:
			if processDataCount == 0:
				x = x[1:-1]
				x = float(x)
				tempRecord.append(x)
				processDataCount += 1
			elif processDataCount == 1:
				processDataCount += 1
				pass
			elif processDataCount == len(line)-1:
				x = x[:-1]
				x = float(x)
				processDataCount += 1
				tempRecord.append(x)
			else:
				x = x[:-1]
				x = float(x)
				tempRecord.append(x)
				processDataCount += 1

		X.append(tempRecord)

X = pd.DataFrame(X)
X = X.T
X = X.as_matrix()

# First time running, create random centroids
centroidList = createRandomCentroids(X)

# This is the list that we will store 'predictions' in and will use for submissions


# Create centroid dictionary to store in cluster number and corresponding values, from there we can go through and pass that dict in to the centroid calculator and
# create new centroids for the clusters
keepDialing = True # Pick Up The Phone And Start Dialing

keepDialingCount = 0

while(keepDialing):
	closestCentroidList = []
	print 'keep dialing'
	keepDialingCount = keepDialingCount +1

	centroidList = createCentroids(centroidDict)
	centroidList = []
	for key, value in centroidDict.iteritems():
		print key, value
		centroidList.append(value)

	print 'centroid list looks like ' , centroidList

	for entry in X:
		entry = np.asarray(entry)
		entryCentroid = 0
		count = 0
		dist = 9999999
		for centroid in centroidList:
			count += 1
			prevDist = dist
			avgEntry = np.asarray(entry)
			dist = distance.euclidean(centroid, np.average(avgEntry))
			print 'dist for centroid ' , str(centroid) , ' is ' , str(dist)
			if dist < prevDist:
				entryCentroid = count
				print 'entryCentroid is now set to ' , str(entryCentroid)




	closestCentroidList.append(entryCentroid)





	if keepDialingCount == 10:
		print 'its false'
		keepDialing = False


resultFile = open('resultFile' , 'wb')
for closestCentroidValue in closestCentroidList:
	resultFile.write(str(closestCentroidValue))
	resultFile.write('\n')
resultFile.close()
