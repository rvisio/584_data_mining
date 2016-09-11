from math import log, sqrt, hypot
import datetime
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

# calculates euclidean distance
def euclid_dist(x_one, y_one, x_two, y_two):
	return hypot(x_two-x_one, y_two - y_one)

# Will contain the training data, sentiment score and the associated words with the score
train_features = []  

# Testing data.  Only contains words, need to predict score
test_features = []  


# TODO
# Possible alternatives
# Build dictionaries for positive and negative reviews, then insert respective words into there. Then find nearest neighbors from there

# Dictionary to count the frequency of words in the total training set 
wordFreq = {}

# Total number of words in the training set
totalWords = 0

# Add the training data to train_features
# Also add words to the word count and frequency dictionary 
with open('../data/cleaned_training.data') as cleaned_data_file:
	for line in cleaned_data_file:
		split_line = line.rsplit('\t')
		sentiment = split_line[0]
		words = split_line[1]
		split_words = words.split()
		for word in split_words: 
			totalWords += 1 
			wordFreq[word] = wordFreq.get(word, 0) + 1

		train_features.append((sentiment, words))

cleaned_data_file.close()

testWordFreq = {}
with open('../data/cleaned_testing.data') as cleaned_testing_file:
	for line in cleaned_testing_file:
		split_line = line.split()
		test_features.append(' '.join(split_line))
		for word in split_line:
			testWordFreq[word] = wordFreq.get(word,0) + 1

# list of sentiment predictions for the test data
# writes to file later on
prediction_results = []

counter = 0  # print something out every so often
# iterates through each test amazon review 
for test_review in test_features:
	if counter % 1000 == 0:
		print counter, ' completed {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

	results = []

	split_testwords = test_review.split()
	
	testScore = 0.0
	for test_word in split_testwords:
		testScore += log(totalWords/testWordFreq[test_word])

	# iterates through each known sentiment + corresponding review
	for train_sentiment, train_words in train_features:
	
		# TODO
		# Work on bigrams, currently taking way too slow
		'''
		trigrams = ngrams(token,3)
		fourgrams = ngrams(token,4)

		print bigrams'''

#		token = nltk.word_tokenize(train_words)

#		bigrams = ngrams(token,2)

		common_words =[]
		# converts the review into a list
		# the review has already been preprocessed in the preprocessing.py file 
		split_trainwords = train_words.split()
		
		trainingScore = 0.0
		commonScore = 0.0

		#checks for common words between the training and test dataset
		for common_word_check in split_trainwords:
			if common_word_check in test_review:
#				print common_word_check
				commonScore += log(totalWords/wordFreq[common_word_check])
			else:
				trainingScore += log(totalWords/wordFreq[common_word_check])
		# TODO
		# New Approach 
		# Create a score for each review  using the same methodology as the below calculation
		# Then use distance algorithim to determine the distance between the two 
		# Common score as x-axis and the overall score as y -axis 

		# calculate the score 
	#	for word in common_words:
			# assign the score
			# log function used to help normalize
	#		commonScore += log(totalWords/wordFreq[word])
			#print 'current word equal ',  word
			#print 'total words = ', str(totalWords) , 'common word dict ', str(wordFreq[word])
		# adds our results to the results list 
		
		# TODO 
		# Distance formula, x1 = training total word score, y1 = common word score, x2 = testing total word score, y2, common word score
		
		totalScore = commonScore + trainingScore
		#print 'COMMON WORD SCORE ' , str(commonScore)
		#print ' TRAINING SCORE ' , str(trainingScore)
		#print 'TEST WORD SCORE ' , str(testScore)
		dist = euclid_dist(trainingScore, commonScore, testScore, commonScore) 
	#	print 'DIST IS EQUAL TO ' , str(dist)
		#results.append((totalScore, train_sentiment))
		results.append((dist, train_sentiment))

	results.sort(reverse=False)
	# counts through the 51 "nearest" neighbors
	toplab = [x[1] for x in results[:101]]

	#print toplab

	# values we're looking for
	numOnes = toplab.count('+1')
	numNeg = toplab.count('-1')

	# Default to negative review due to some reviews being blank
	# But they are classified as negative reviews 
	prediction = '-1'

	if numOnes > numNeg:
		prediction = '+1'

	prediction_results.append(prediction)
	counter += 1


# write the results
resultsFile = open('../data/results.data', 'wb')

for x in prediction_results:
	resultsFile.write(x)
	resultsFile.write('\n')

resultsFile.close()
