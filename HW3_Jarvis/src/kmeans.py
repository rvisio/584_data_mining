import numpy as np
import random
from scipy.spatial import distance
#from sklearn.cluster import KMeans
k = 3
#TODO 
# add method to check centroid averages and return new centroids 
# 
def createCentroids(array, firstRun):
	if firstRun == True:
		# get the max and min values, will be used for randomly creating centrodis
		maxValue =5
		minValue =5
		for record in X:
			print record
			print np.average(record)
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
			centroidList.append((round(random.uniform(minValue, maxValue), 2),round(random.uniform(minValue, maxValue), 2),round(random.uniform(minValue, maxValue), 2),round(random.uniform(minValue, maxValue), 2)))

		return np.asarray(centroidList)
	
	# not randomly generating centroids, need to caclulate them based off of the array being passed in 
	else:


X = []

# Read data in 
with open('../iris.data') as irisData:
	for line in irisData:
		line = line.split()
		tempRecord = []
		for x in line:
			x = float(x)
			tempRecord.append(x)

		X.append(tempRecord)

X = np.asarray(X, dtype=float)
print ('we made it')


centroidList = createCentroids(X, True)


closestCentroidList = []
# Compare values to centroids

#Pick up the phone and start dialing
keepDialing = True
while(keepDialing):
	for entry in X:
		entry = np.asarray(entry)
		entryCentroid = 0
		count = 0
		dist = 9999999
		for centroid in centroidList:
			count += 1 
			prevDist = dist
			dist = distance.euclidean(centroid, entry)
			
			if dist < prevDist:
				entryCentroid = count

		closestCentroidList.append(entryCentroid)


resultFile = open('resultFile' , 'wb') 
for x in closestCentroidList:
	resultFile.write(str(x))
	resultFile.write('\n')
resultFile.close()
