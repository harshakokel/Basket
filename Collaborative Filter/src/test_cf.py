import math
import numpy as np

def predict_rating(CF, user, movie):
    prediction = 0
    weights = []
    for i in range(len(CF.rating_matrix)):
        if CF.rating_matrix[i][movie] is None:
            continue
        weight = CF.correlation(user, i)
        if weight is None or weight == 0:
            continue
        weights.append(weight)
        prediction += weight*(CF.rating_matrix[i][movie] - CF.mean_vote[i])
    if prediction == 0:
        return prediction + CF.mean_vote[user]
    prediction = prediction/sum([abs(x) for x in weights])
    prediction += CF.mean_vote[user]
    return prediction


def test(CF, filename):
    header = ['movieID', 'customerID', 'rating']
    data = np.recfromcsv(filename, names=header, case_sensitive=True)
    absolute_mean = 0
    root_mean_squared = 0
    for row in data:
        user = CF.customers.index(row[header[1]])
        movie = CF.movies.index(row[header[0]])
        predict = predict_rating(CF, user, movie)
        print ("row: ", row, " predicted: ", predict,)
        x = (predict - row[header[2]])
        absolute_mean += abs(x)
        root_mean_squared += math.pow(x, 2)
    print(absolute_mean, " absolute mean")
    print(math.sqrt(root_mean_squared), " square  mean")
    return data
