import numpy as np 
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


# read in and create numpy array ( np.array) 
# will need to store the classification in separate value and numpy array in some sort of table
X = []
y = []


# Go through cleaned up csv 
f = open('cleaned_training.csv', 'rt')
try:
	reader = csv.reader(f)
	next(reader,None)
	for row in reader:
		features = []
		classifier = row[0]

		for x in row[1:]:
			features.append(x)
		X.append(list(features))
		y.append(classifier)

finally:
	f.close()


# Convert to numpy array and change data type to float to solve issue 
X = np.array(X,dtype=float)
X_new = SelectKBest(chi2, k=20).fit_transform(X,y)


#----------------------------------------
# Other random models included below
# Keeping them in the code for when I come back later and fool around with it
#----------------------------------------

#knn = KNeighborsClassifier(n_neighbors=3)
#knn.fit(X,y)

rf = RandomForestClassifier(n_estimators=64)
rf.fit(X,y)

#clf = BernoulliNB()
#npArrayX  = np.asarray(X, dtype=np.s32)
#npArrayY = np.asarray(y, dtype=np.s32)

#clf.fit(npArrayX, npArrayY)

# Get the testing features
test_features = []
test_file = open('cleaned_testing.csv', 'rt')
try:
	reader = csv.reader(test_file)
	next(reader,None)
	for row in reader:
		features = []

		for x in row:
			features.append(x)
		test_features.append(list(features))

finally:
	test_file.close()

print 'about to predict'
#predict_results = knn.predict(test_features)
#print len(test_features)
predict_results = rf.predict(test_features)
#predict_results = knn.predict(test_features)
#predict_results = clf.predict(test_features)

#print predict_results
#print len(predict_results)


# Convert to numpy arary and run some feature reduction 
test_features = np.array(test_features,dtype=float)
test_features_new = SelectKBest(chi2,k=20).fit_transform(test_features,predict_results)
new_rf = RandomForestClassifier(n_estimators=64)
#new_knn = KNeighborsClassifier(n_neighbors=3)
new_rf.fit(X_new,y)
#new_knn.fit(X_new,y)
new_predict_results = new_rf.predict(test_features_new)
#new_predict_results = new_knn.predict(test_features_new)

#print new_predict_results

#f1_score_predict = rf.predict(test_features)

#print 'lets check the f1 score'
#print f1_score(f1_score_predict, y, pos_label='0', average = 'binary')

# Lets calculate the F1 Score 
rf_f1_score = RandomForestClassifier(n_estimators=64)

#knn_f1_score = KNeighborsClassifier(n_neighbors=3)

rf_f1_score.fit(test_features_new,predict_results)
#knn_f1_score.fit(test_features_new,predict_results)
f1_results = rf_f1_score.predict(X_new)
#f1_results = knn_f1_score.predict(X_new)

print 'F1-SCORE HERE'
print f1_score(f1_results,y, pos_label='1',average='binary')

resultsFile = open('new_results.data', 'wb')
for x in new_predict_results:
	resultsFile.write(x)
	resultsFile.write('\n')

