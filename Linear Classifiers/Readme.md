This project was implemented using python ** (version 3) ** as part of Homework-2 in CS 6375 Machine Learning at University of Texas at Dallas in Spring 2018 by Harsha Kokel.

This homework asked for implementation of three classifiers: Naive Bayes, Logistic Regression and Perceptron for  Spam/Ham classification problem.
Three data sets were provided for this problems.

**NOTE** For all the data sets, the training folder should have two folders with the class names. In all the example usages below, `data/data_set_1/train` is a training folder, so `/train` has two folders `/ham` and `/spam` inside  `/train`. Similarly, the testing folder `data/data_set_1/test` also has two folders `/ham` and `/spam` inside  `/test`.

### 1. Naive Bayes
This classifier uses bag-of-words model to calculate the prior & conditional probabilities and uses these probabilities to determine the class of the test example. I tried removing the stopwords but found that removing the stop words reduces the accuracy.

Running Naive Bayes classifier on the three data sets resulted in following accuracies:


| Data Set | Accuracies |
| ------------- |:---------: |
| data_set_1 | 94.98 |
| data_set_2 | 91.88 |
| data_set_3 | 93.73 |

##### Usage

* In python3 console, import the Naive Bayes library. Make sure you have naive_bayes.py and classifier.py in the location where you initiate the python console.

```python
$ python3
>>> from naive_bayes import NaiveBayes
```

* Create a Naive Bayes classifier and Train it by using `train` function. This takes path to the training folder as argument.

```python3
>>> NB = NaiveBayes()
>>> NB.train("../data/data_set_3/train")
```


* Test the Naive Bayes on the testing data using `test` function. This function takes path to the testing folder as argument.

```python3
>>> NB.test("../data/data_set_3/test")
Correct Prediction:  509 / 543
Accuracy:  93.73848987108656
```


### 2. Logistic Regression

This classifier is implemented in `logistic_regrssion.py` file. inside `/src` folder. This classifier treats lambda as hyper parameter and learns that for three data set using 70/30 split for training/validation data. The LogR classifiers updates the weight using gradient ascent which is a batch algorithm. It continues updating the values for 100 iterations. Learning rate used was 0.05.

Running this perceptron on the three data sets resulted in following accuracies:



| Data Set | Accuracies | Lambda |   
| ------------- |:---------: | :-----:|  
| data_set_1 | 96.72 | 0.1 |  
| data_set_2 | 94.6 | 0.1 |
| data_set_3 | 92.7 | 0.1 |


##### Usage
* In python3 console, import the LogisticRegression library. Make sure you have logistic_regrssion.py and classifier.py in the location where you initiate the python console.

```python
$ python3
>>> from logistic_regression import LogisticRegression
```

* Create a LogR classifier and Train it by using `train_and_learn` function. This takes path to the training folder and Candidate values of Lambda as input argument. This function treats `lambda` as hyper parameter, it splits the data into Training & Validation set and learns the `lambda`. After learning the hyper parameter, it uses the full training set to train the LogR.  

```python
>>> LogR = LogisticRegression()
>>> lambda_candidates = [0.01, 0.05, 0.1, 1, 5, 10]
>>> LogR.train_and_learn("../data/data_set_1/train", lambda_candidates)
```

* Test the LogR classifier on the testing data using `test` function. This function takes path to the testing folder as argument.

```python3
>>> LogR.test("../data/data_set_1/test")
lambda  1
learning rate:  0.05
Prediction:  348 / 478
Accuracy:  72.80334728033473
log likelihood:  -791.3085215876044
```


### 3. Perceptron

This classifier is implemented in `perceptron.py` file inside `/src` folder. This classifier treats number of iterations as hyper parameter and learns that for three data set using 70/30 split for training/validation data. The perceptron classifiers updates the weight after predicting each example and continues this till all the examples in the training set are classified correctly. In case of non-linearly seperable data perceptron may never be able to classify all the data correctly, So we have used a hard bound of 50 iteration. In case all examples are not classified correctly even after 50 iterations, perceptron will end the learning and simply use the weights updated in 50th iteration. Learning rate used was 0.005.

Running this perceptron on the three data sets resulted in following accuracies:



| Data Set | Accuracies | No of iterations |   
| ------------- |:---------: | :-----:|  
| data_set_1 | 95.60 | 5 |  
| data_set_2 | 93.20 | 4 |
| data_set_3 | 96.13 | 3 |




##### Usage
* In python3 console, import the Perceptron library. Make sure you have perceptron.py and classifier.py in the location where you initiate the python console.

```python
$ python3
>>> from perceptron import Perceptron
```



* Create a perceptron and Train it by using `train_and_learn` function. This takes path to the training folder as argument. This function treats `no of iteration` as hyper parameter, it splits the data into Training & Validation set and learns the `no of iteration`. After learning the hyper parameter, it uses the full training set to train the perceptron.  


```python
>>> P = Perceptron()
>>> P.train_and_learn("../data/data_set_1/train")
Reading training data:  ../data/data_set_1/train
Learning begins
iteration 1
Correct Prediction:  125 / 139
Accuracy:  89.92805755395683
iteration 2
Correct Prediction:  135 / 139
Accuracy:  97.12230215827338
iteration 3
Correct Prediction:  135 / 139
Accuracy:  97.12230215827338
iteration 4
Correct Prediction:  134 / 139
Accuracy:  96.40287769784173
iteration 5
Correct Prediction:  134 / 139
Accuracy:  96.40287769784173
Best accuracy 135
Best Iteration 3
Learning ends
Training begins
Training iteration:  0
Training iteration:  1
Training iteration:  2
Training ends
```

If we already know the hyper parameter, `no of iteration`, then we can use function `train` directly   

```python
>>> P.train("../data/data_set_1/train", 10)
Training begins
Training iteration:  0
Training iteration:  1
Training iteration:  2
Training iteration:  3
Training iteration:  4
Training iteration:  5
Training iteration:  6
Training iteration:  7
Training iteration:  8
Training iteration:  9
Training ends
```




* Test the perceptron on the testing data using `test` function. This function takes path to the testing folder as argument.

```python3
>>> P.test("../data/data_set_1/test")
Reading testing data:  ../data/data_set_1/test
Testing begins
Correct Prediction:  443 / 478
Accuracy:  92.67782426778243
Testing ends
```

* To check prediction of a single example (mail in our case), we can use function `test_example`. This function takes the file as input argument and returns the predicted class.

```python3
>>> P.test_example("../data/data_set_1/test/ham/0003.1999-12-14.farmer.ham.txt")
'ham'
```

### Report

The accuracies obtained on various test sets are given above. The Lambda values help us regularize the weights learned, so higher the lambda smaller the weights, but that reduces the accuracy as well. so, We need to make sure lambda is not too small and not too big. Learning rate drives the move over the gradient. Higher the value more the weight will move towards the gradient but this makes the weight skip in a sense that it misses the minima and jumps to other side of the curve. So we need to make sure the learning rate is small enough so that the values converge soon but not too big.
