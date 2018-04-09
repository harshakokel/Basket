"""Module represents Collaborative Filter."""
import math
import sys
from datetime import datetime
import numpy as np

class CollaborativeFilter(object):

    def processing_netflix_file(self, filename):
        header = ['movieID', 'customerID', 'rating']
        data = np.recfromcsv(filename, names=header, case_sensitive=True)
        self.movies = list(set(data[header[0]]))
        self.customers = list(set(data[header[1]]))
        self.rating_matrix =  [[None for i in range(len(self.movies))] for j in range(len(self.customers))]
        for row in data:
            self.rating_matrix[self.customers.index(row[header[1]])][self.movies.index(row[header[0]])] = row[header[2]]
        self.find_mean_vote()
        self.cache_correlation = {}

    def find_mean_vote(self):
        self.mean_vote = []
        i = 0
        for customer in self.rating_matrix:
            ratings = list(filter(None.__ne__, customer))
            self.mean_vote.append(sum(ratings)/len(ratings))


    def correlation(self, user_a, user_i):
        """Correlation between two users."""
        if user_a > user_i:
            temp = user_a
            user_a = user_i
            user_i = temp
        key = str(user_a)+"_"+str(user_i)
        if key in self.cache_correlation:
            return self.cache_correlation[key]
        ratings_a = self.rating_matrix[user_a]
        ratings_i = self.rating_matrix[user_i]
        rating = list(filter(lambda x: all(i is not None for i in x), zip(ratings_a, ratings_i)))
        if rating is None or len(rating) == 0:
            return None
        numerator = 0
        denominator_a = 0
        denominator_i = 0
        mean_a = self.mean_vote[user_a]
        mean_i = self.mean_vote[user_i]
        for movie in rating:
            numerator += (movie[0] - mean_a)*(movie[1] - mean_i)
            denominator_a += math.pow((movie[0] - mean_a), 2)
            denominator_i += math.pow((movie[1] - mean_i), 2)
        if numerator == 0:
            self.cache_correlation[key] = 0
        else:
            self.cache_correlation[key] = numerator/math.sqrt(denominator_a*denominator_i)
        return self.cache_correlation[key]


    def predict(self, user, movie):
        prediction = 0
        weights = []
        for i in range(len(self.rating_matrix)):
            if self.rating_matrix[i][movie] is None:
                continue
            weight = self.correlation(user, i)
            if weight is None or weight == 0:
                continue
            weights.append(weight)
            prediction += weight*(self.rating_matrix[i][movie] - self.mean_vote[i])
        if prediction == 0:
            return prediction + self.mean_vote[user]
        prediction = prediction/sum([abs(x) for x in weights])
        prediction += self.mean_vote[user]
        return prediction

    def test(self, filename):
        header = ['movieID', 'customerID', 'rating']
        data = np.recfromcsv(filename, names=header, case_sensitive=True)
        absolute_mean = 0
        root_mean_squared = 0
        for row in data:
            user = self.customers.index(row[header[1]])
            movie = self.movies.index(row[header[0]])
            predict = self.predict(user, movie)
            print ("Predicted: ", predict, ", original: ", row[header[2]])
            absolute_mean += abs(predict - row[header[2]])
            root_mean_squared += math.pow((predict - row[header[2]]), 2)
        print(absolute_mean, " absolute mean")
        print(math.sqrt(root_mean_squared), " square  mean")
        return data

# Driver code
print(str(datetime.now()))
train = "../data/netflix/TrainingRatings.txt"
test = "../data/netflix/TestingRatings.txt"
CF = CollaborativeFilter()
CF.processing_netflix_file(train)
print("Train file read ",str(datetime.now()))
test_data = CF.test(train)
print(str(datetime.now()))
