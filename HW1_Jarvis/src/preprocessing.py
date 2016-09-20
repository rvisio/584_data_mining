import nltk
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer

stop_words = set(stopwords.words('english'))

# Clean up text reviews 
def cleanReview(review):
	cleanReview = []
	review = review.lower()  # make everything lower case
	review = review.translate(string.maketrans("",""),string.punctuation)  # remove all punctuation
	review = review.split()  # split er up

	
	# remove stop words
	for word in review:
		if word not in stop_words:
			# get just the stem of the word
			word = PorterStemmer().stem_word(word)
			cleanReview.append(word)

	return cleanReview

		
		

cleanDataFile = open("../data/cleaned_training.data", "wb")


# Reads the unclean training data, then writes the new/clean results to a new file 
with open('../data/1472237399_7021325_train_file.data') as uncleanTrainingData:
	for line in uncleanTrainingData:
		split_line = line.rsplit('\t')
		sentiment = split_line[0]
		unclean_review = split_line[1]
	
		cleaned_review = cleanReview(unclean_review)
		
		cleanDataFile.write(sentiment)
		cleanDataFile.write('\t')
		cleanDataFile.write(' '.join(cleaned_review))
		cleanDataFile.write('\n')

cleanDataFile.close()
uncleanTrainingData.close()


cleanTestFile = open ("../data/cleaned_testing.data", "wb")

with open('../data/1472237399_726165_test.data') as uncleanTesting:
	for line in uncleanTesting:
		cleaned_testing = cleanReview(line)

		cleanTestFile.write(' '.join(cleaned_testing))
		cleanTestFile.write('\n')

cleanTestFile.close()
uncleanTesting.close()
