import pandas as pd 
import numpy as np 

# pandasList is a list that will be converted to a dataframe after the training and testing file have been processed
pandasList = []
newTrainFeatureList = []
# Dictionary to count the number of times compounds appear in the testing and training dataset
compoundDict = {}

# Iterate through the training file
with open('train.data') as training_file:
	for line in training_file:
		split_line = line.rsplit('\t')

		classifier = split_line[0]
		compounds = split_line[1]
		
		# add compounds to the dictionary
		for compound in compounds.split():
			compoundDict[compound] = compoundDict.get(compound,0) + 1
	
		# create tuple 
		record = (classifier, compounds)		
		
		# append tuple to the pandas list and to the new feature list
		pandasList.append(record)
		newTrainFeatureList.append(record)

training_file.close()

newTestFeatureList = []
with open('test.data') as testing_file:
	for line in testing_file:
		pandasList.append((line))
		newTestFeatureList.append((line))
		for compound in line.split():
			compoundDict[compound] = compoundDict.get(compound,0)+1
testing_file.close()

df = pd.DataFrame(pandasList)

# Iterate through the compound dictionary and append values if they're greater than our threshold
# Not sure if this is the best way to get features. Probably something better using an external library 
# Ultimate goal is to keep the compounds that are appearing frequently, they'll probably have more weight on the dataset 
threshold = 25
compoundsToKeep = []
for key, value in compoundDict.iteritems():
	if value > threshold and key not in compoundDict.values():
		compoundsToKeep.append(key)

# Create header for the new data frame 
compoundHeader = 'compound_'
header = ['classifier']
for compound in compoundsToKeep:
	compoundStr = compoundHeader + compound
	header.append(compoundStr)


# Convert our original training file and testing file to our new format
#cleanTrainFile = open('cleaned_train.data', 'wb')

newRecords = []
for record in newTrainFeatureList:
	curRecord = []
	
	# append the classifier to the front of the new record
	curRecord.append(record[0])

	observedCompounds = (record[1].split())

	for comp in compoundsToKeep:
		if comp in observedCompounds:
			curRecord.append(1)
		else:
			curRecord.append(0)
	newRecords.append(curRecord)
# convert to pandas dataframe and write to csv
cleaned_training_df = pd.DataFrame(newRecords)
cleaned_training_df.to_csv('cleaned_training.csv', header=header, index=False)

newRecords = []
for record in newTestFeatureList:
	curRecord = []

	observedCompounds = (record.split())

	for comp in compoundsToKeep:
		if comp in observedCompounds:
			curRecord.append(1)
		else:
			curRecord.append(0)
	newRecords.append(curRecord)
	
# convert to pandas dataframe and write to csv
cleaned_testing_df = pd.DataFrame(newRecords)
cleaned_testing_df.to_csv('cleaned_testing.csv', header=header[1:], index = False)
