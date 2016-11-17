from sklearn.neighbors import NearestNeighbors
import numpy as np
import knn_util as ku
import sys

X = []
movieIndex = [] # index for looking up movieId position in the knn result

with open ('data/additional_files/matrix.dat') as genres:
    for line in genres:
        line = line.strip()
        line = line.split()
        movieIndex.append(line[0])
        X.append(line[1:])
genres.close()

X = np.array(X)

nbrs = NearestNeighbors(n_neighbors=10, algorithm='brute',metric='cosine').fit(X)

distances, indices = nbrs.kneighbors(X)

print movieIndex[9909] # the movie id corresponding to indeces[9909]
print indices[9909] # gives us the nearest neighbors (corresponding indexes) need to use movieIndex to find them
print movieIndex[6551] # movie id for nearest neighbor






#TODO
# add a way to check if user has already review for the nearest neighbor, then just use that value

# counter = 0
# predictionList = []
# with open ('data/test.dat') as testFile:
#     for line in testFile:
#         line = line.split()
#         userId = line[0]
#         movieId = line[1]
#
#         try:
#             # Find nearest neighbor for movieId
#             #print movieId, ' ' , movieIndex.index(movieId), ' ', indices[movieIndex.index(movieId)][0], ' ' , movieIndex[indices[movieIndex.index(movieId)][0]]
#             nearestNeighborIndex = indices[movieIndex.index(movieId)]
#             #print nearestNeighborIndex
#             reviewList = []
#             for nn in nearestNeighborIndex:
#                 nearestNeighborMovieId = movieIndex[nn]
#                 reviewList.append(np.mean(ku.getAverageRating(nearestNeighborMovieId)))
#
#             reviewList = np.array(reviewList)
#             predictionList.append(str(round(np.mean(reviewList),1)))
#             # get ratings list of movieId
#             #print indices[movieIndex.index(movieId)][0]
#             # reviewList = ku.getAverageRating(nearestNeighborMovieId)
#             #
#             # predictionList.append(str(round(np.mean(reviewList), 1)))
#
#
#             # average all ratings for the nearestNeighborMovieId
#
#             # append rating to prediction list and later write this list to file
#
#         except:
#             print sys.exc_info()[0]
#             predictionList.append('3.0')
#
# testFile.close()

counter = 0
predictionList = []
with open ('data/test.dat') as testFile:
    for line in testFile:
        line = line.split()
        outputList = []
        userId = line[0]
        movieId = line[1]

        try:
            # Find nearest neighbor for movieId
            #print movieId, ' ' , movieIndex.index(movieId), ' ', indices[movieIndex.index(movieId)][0], ' ' , movieIndex[indices[movieIndex.index(movieId)][0]]
            nearestNeighborIndex = indices[movieIndex.index(movieId)]
            #print nearestNeighborIndex
            reviewList = []
            for nn in nearestNeighborIndex:
                nearestNeighborMovieId = movieIndex[nn]
                reviewList.append(np.mean(ku.getAverageRating(nearestNeighborMovieId)))

            reviewList = np.array(reviewList)
            predictionList.append(str(round(np.mean(reviewList),1)))
            # get ratings list of movieId
            #print indices[movieIndex.index(movieId)][0]
            # reviewList = ku.getAverageRating(nearestNeighborMovieId)
            #
            # predictionList.append(str(round(np.mean(reviewList), 1)))


            # average all ratings for the nearestNeighborMovieId

            # append rating to prediction list and later write this list to file

        except:
            print sys.exc_info()[0]
            predictionList.append('4.0')


testFile.close()


predictionFile = open('data/predict.dat', 'wb')

for p in predictionList:
    predictionFile.write(p[0])
    predictionFile.write(' ')
    predictionFile.write(p[1])
    predictionFile.write('\n')



