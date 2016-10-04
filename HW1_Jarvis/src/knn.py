from math import log, sqrt, hypot
import datetime
import nltk
from nltk import word_tokenize

# Will contain the training data, sentiment score and the associated words with the score
train_features = []  

# Testing data.  Only contains words, need to predict score
test_features = []  

# Dictionary to count the frequency of words in the total training set 
wordFrequency = {}

# Total number of words in the training set
totalWords = 0

# Add the training data to train_features
# Also adds all training words to dictionary, and counts total words
with open('../data/cleaned_training.data') as cleaned_data_file:
	for line in cleaned_data_file:
		split_line = line.rsplit('\t')
		sentiment = split_line[0]
		words = split_line[1]
		split_words = words.split()
		for word in split_words: 
			totalWords += 1 
			wordFrequency[word] = wordFrequency.get(word, 0) + 1
		
		# Append to list as tuple
		train_features.append((sentiment, words))
cleaned_data_file.close()

with open('../data/cleaned_testing.data') as cleaned_testing_file:
	for line in cleaned_testing_file:
		split_line = line.split()
		test_features.append(' '.join(split_line))

# list of sentiment predictions for the test data
# writes to file later on
prediction_results = []

counter = 0  # print something out every so often
# iterates through each test amazon review 
for test_review in test_features:
	if counter % 100 == 0:
		print counter, ' completed {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

	results = []

	split_testwords = test_review.split()
	
	# iterates through each known sentiment + corresponding review
	for train_sentiment, train_words in train_features:
	
		common_words =[]
		# converts the review into a list
		# the review has already been preprocessed in the preprocessing.py file 
		split_trainwords = train_words.split()
		
		commonScore = 0.0

		#checks for common words between the training and test dataset
		for common_word_check in split_trainwords:
			# check for the common word within the test review 
			if common_word_check in test_review: 
				# increase the score 
				commonScore += log(totalWords/wordFrequency[common_word_check])

		# Append results to list so that we can check neighbors	
		results.append((commonScore, train_sentiment))
	
	# Reverse sort so that we can have the greatest values at the top 
	# Since we are perfroming a similarity score we want to see high similarity scores 
	# If using euclidean distance or other distance metric, would want to see low distance scores
	results.sort(reverse=True)
	
	top_results = []
	# Select the nearest neighbors here 
	# Set the number of 'neighbors' based off the results[:X] list 
	for neighbor in results[:101]:
		top_results.append(neighbor)

	# values we're looking for
	# Count method makes that easy for us 
	positive_reviews = top_results.count('+1')
	neg_reviews = top_results.count('-1')

	# Default to negative review due to some reviews being blank
	# But they are classified as negative reviews 
	prediction = '-1'

	# Assign positive sentiment if there are more 
	if positive_reviews > neg_reviews:
		prediction = '+1'
	
	# Add sentiment to the results 
	prediction_results.append(prediction)
	counter += 1


# write the results to file for submission
resultsFile = open('../data/results.data', 'wb')

for x in prediction_results:
	resultsFile.write(x)
	resultsFile.write('\n')

resultsFile.close()
