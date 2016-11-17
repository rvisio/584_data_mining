from sklearn.neighbors import NearestNeighbors
import numpy
from sklearn.externals import joblib
from collections import Counter
import math

genre_dict = {}
train_dict = {}
def removeGenres(genre_list):

    with open('data/additional_files/movie_genres.dat') as genres:
        for line in genres:
            line = line.split()
            genre_dict.setdefault(line[0],[]).append(line[1])
    genres.close()


    # Goal is to cut down on all the different movie types
    # iterating through the genre_list and only going to keep movies that exist in that list
    movieIdList = []
    with open('data/additional_files/train.dat') as train:
        for line in train:
            line = line.split()
            movieId = line[1]

            movieGenre = genre_dict.get(movieId)
            for genre in movieGenre:
                if genre in genre_list:
                    train_dict[int(line[0])] = [int(line[1]), float(line[2])]
                    movieIdList.append([int(line[0]),int(line[1]),float(line[2])])


    train.close()
    movieList = [movieIdList[i] for i in range(len(movieIdList)) if i == 0 or movieIdList[i] != movieIdList[i - 1]]

    file = open('data/additional_files/trimmed_train.dat', 'wb')
    for x in movieList:
        file.write(str(x[0]))
        file.write(' ')
        file.write(str(x[1]))
        file.write(' ')
        file.write(str(x[2]))
        file.write('\n')
    file.close()


def predict():
    predictionList = []
    createMovieRatingDict()

    with open('data/test.dat') as testFile:
        for line in testFile:
            line = line.split()
            testMovieId = str(line[1])
            try:
                reviewList = movieRatingsDict[testMovieId]
                predictionList.append(str(round(numpy.mean(reviewList),1)))

            except:
                predictionList.append('3.0')


    predictionFile = open('data/predict.dat', 'wb')
    for x in predictionList:
        predictionFile.write(x)
        predictionFile.write('\n')




def getUserRating(userId,movieId):
    if len(userRatingDict.keys()) == 0:
        print ' creating user rating dict '
        createUserRatingDict()
        print 'done'
    print 'returning list for ' , userId , ' ' , movieId
    print type(userRatingDict[userId])
    print userRatingDict[userId]
    return userRatingDict[userId][movieId]


userRatingDict = {}
def createUserRatingDict():
    with open('data/additional_files/train.dat') as trainingFile:
        for line in trainingFile:
            line = line.split()
            userId = str(line[0])
            movieId = str(line[1])

            if userId not in userRatingDict:
                userRatingDict[userId] = [{movieId : [float(line[2])]}]

            if movieId in userRatingDict[userId]:
                userRatingDict[userId][movieId].append(float(line[2]))
            elif movieId not in userRatingDict[userId]:
                userRatingDict[userId].append({movieId : [float(line[2])]})

    trainingFile.close()



def getAverageRating(movieId):
    if len(movieRatingsDict.keys()) == 0:
        print 'creating movie ratings dict'
        createMovieRatingDict()

    return movieRatingsDict[movieId]

movieRatingsDict = {}
def createMovieRatingDict():
    with open('data/additional_files/train.dat') as trainingFile:
        for line in trainingFile:
            line = line.split()
            movieId = str(line[1])
            if movieId in movieRatingsDict:
                movieRatingsDict[movieId].append(float(line[2]))
            else:
                movieRatingsDict[movieId] = [float(line[2])]
    print len(movieRatingsDict)
    trainingFile.close()



def createDirectorCsv():

    with open('genres.csv') as genres:
        movieIdList = []
        for line in genres:
            line = line.split(',')

            movieIdList.append(str(line[0]))
            print line[0]
    genres.close()


    directorId = 0
    newDirCsv = []
    newDirFile =  open('data/additional_files/directors.csv', 'wb')
    counter = 0
    with open('data/additional_files/movie_directors.dat.latin1.dat') as dirFile:
        for line in dirFile:
            line = line.split()
            movieId = line[0]
            if str(movieId) in movieIdList:
                counter += 1
                directorId += 1

                newDirFile.write(movieId)
                newDirFile.write(' ')
                newDirFile.write(str(directorId))
                newDirFile.write('\n')
            else:
                print line[0]
                print 'movie id not found'

    dirFile.close()
    newDirFile.close()
    print counter

def createNewSuperMatrix():
    newMatrix = open('data/additional_files/matrix.dat' , 'wb')
    with open('data/additional_files/directors.csv') as directors:
        dirColumns = []
        for dirLine in directors:
            dirLine = dirLine.split()
            dirColumns.append((dirLine[0],dirLine[1]))

    print len(dirColumns)
    directors.close()

    with open('genres.csv') as genres:
        for gLine in genres:
            gLine = gLine.strip()
            gLine = gLine.split(',')

            for dir in dirColumns:
                if dir[0] == gLine[0]:
                    gLine.append('1')
                else:
                    gLine.append('0')


            for x in gLine:
                newMatrix.write(str(x))
                newMatrix.write(' ')
            newMatrix.write('\n')

    directors.close()


def getMode():
    newList = []
    with open('data/additional_files/train.dat') as predict:
        for line in predict:
            line = line.split()
            newList.append(float(line[2]))

    count = Counter(newList)

    print count





if __name__ == '__main__':
    #removeGenres(('Action', 'Adventure', 'Drama', 'Comedy'))
    #predict()
    #createDirectorCsv()
    #createNewSuperMatrix()
    getMode()










