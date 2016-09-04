from math import log, sqrt
import time

train_features = []  # read this from the cleaned up data set
test_features = []  # this will be read from the features we will be testing, does not need the whole review in there. just +1 or -1

# count the frequency of words, this will be weighted when determining relevancy 
commonWords = {}
counter = 0
with open('../data/cleaned_training.data') as cleaned_data_file:
	for line in cleaned_data_file:
		split_line = line.rsplit('\t')
		sentiment = split_line[0]
		words = split_line[1]
		split_words = words.split()
		for word in split_words: 
			counter += 1 
			commonWords[word] = commonWords.get(word, 0) + 1

		train_features.append((sentiment, words))

cleaned_data_file.close()

sanityCheck = 0 
with open('../data/cleaned_testing.data') as cleaned_testing_file:
	for line in cleaned_testing_file:
		split_line = line.split()
		test_features.append(' '.join(split_line))

prediction_results = []
for test_review in test_features:
	#print x
	if sanityCheck % 100 == 0:
		print sanityCheck, ' completed' , str(time.time())

	results = []
	for train_sentiment, train_words in train_features:
		#print 'printing the training sentiment ', train_sentiment
		#print 'printing the training words ' , train_words
		split_trainwords = train_words.split()
		common_words = [x for x in split_trainwords if x in test_review]
		score = 0.0
		for word in common_words:
			score += log(counter/commonWords[word])
		results.append((score, train_sentiment))

	results.sort(reverse=True)
	
	toplab = [x[1] for x in results[:5]]


	numOnes = toplab.count('+1')
	numNeg = toplab.count('-1')
	
	prediction = '+1'

	if numNeg > numOnes:
		prediction = '-1'
	prediction_results.append(prediction)
	sanityCheck += 1

print len(test_features)

resultsFile = open('../data/results.data', 'wb')

for x in prediction_results:
	resultsFile.write(x)
	resultsFile.write('\n')

resultsFile.close()
