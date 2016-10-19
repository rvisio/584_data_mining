from itertools import izip
# Function to iterate through list elements two at a time
def pairwise(iterable):
	a = iter(iterable)
	return izip(a,a)

# Counting the number of times feature appear, store the values in this dictionary 
# Then check the frequency of featuers and store applicable results in finalFeatureCount
featureCount = {}
inputDictionary = {}
counter = 0
with open('../data/input.mat') as input_file:
	for line in input_file:
		counter += 1
		line = line.split()
		inputDictionary[counter] = line 
		for x,y in pairwise(line):
			featureCount[x] = featureCount.get(x,0)+1
finalFeatureCount = []
for key,value in featureCount.iteritems():
	if value >= 150:
		#print type(key)
		finalFeatureCount.append(key)

# finalFeatureCount holds our features that appear more than 300 times 
finalFeatureCount = tuple(finalFeatureCount)
#Create dictionary of the feature id's and their corresponding words
featureCounter = 0
featureDictionary = {}
with open('../data/features.label') as features:
	for line in features:
		line = line.strip()
		featureCounter += 1
		#print type(finalFeatureCount)
		if str(featureCounter) in finalFeatureCount:
			featureDictionary[featureCounter] = line
#masterDF = pd.DataFrame.from_dict(featureDictionary,'index')
#print masterDF
matrix = []

for feature in finalFeatureCount:
	print 'currently on ' , str(feature)
	tempRecord = []
	tempRecord.append(feature)
	tempRecord.append(featureDictionary[int(feature)])
	
	# Iterate through the records, set values for records
	for key, value in inputDictionary.iteritems():
		#tempRecord.append(key)
		if feature in value and value.index(feature) % 2 == 0:
			tempRecord.append(value[value.index(feature)+1])

		else:
			tempRecord.append(0)



	matrix.append(tuple(tempRecord))

cleaned_data = open('../data/features.data', 'wb')

for x in matrix:
	cleaned_data.write(str(x))
	cleaned_data.write('\n')

cleaned_data.close()

