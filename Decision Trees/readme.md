# Decision Tree 

This code is implemented as part of Homework 1 in CS 6375 Machine Learning Course at The University of Texas at Dallas.

The assignment was to implement Decision Tree Learning algorithm. This was divided into two parts. First part was learning the tree from training set and second part was pruning the tree based on validation set. The data set used for this development is available [here](http://www.hlt.utdallas.edu/~vgogate/ml/2018s/homeworks.html). Each data set is divided into three sets: the training set, the validation set and the test set. Data sets are in CSV format. The first line in the file gives the attribute names. Each line after that is a training (or test) example that contains a list of attribute values separated by a comma. The last attribute is the class-variable. Assume that all attributes taken values from the domain {0,1}.

##### Learning Tree
The following two heuristics are implemented for selecting the next attribute:

1. Information gain heuristic (mentioned in [Mitchell, Tom M.](http://www.cs.cmu.edu/~tom/) (1997) [Machine Learning](https://www.cs.cmu.edu/~tom/mlbook.html))
2. Variance impurity heuristic described below.  
Let K denote the number of examples in the training set. Let K0 denote the number of training examples that have class = 0 and K1 denote the number of training examples that have class = 1. The variance impurity of the training set S is defined as

```math
VI(S) = \frac{K0}{K} * K1/K
```

Notice that the impurity is 0 when the data is pure. The gain for this impurity is defined as usual

 ![alt text](https://github.com/harshakokel/Machine-Learning/blob/master/Assets/information-gain-equation.png "Information Gain equation")

where X is an attribute, Sx denotes the set of training examples that have X = x and Pr(x) is the fraction of the training examples that have X = x (i.e., the number of training examples that have X = x divided by the number of training examples in S).

##### Pruning Tree
Implement Post Pruning algorithm as given below.

##### Usage
.\program <L> <K> <training-set> <validation-set> <test-set> <to-print>

L: integer (used in the post-pruning algorithm)
K: integer (used in the post-pruning algorithm)
to-print:{yes,no}

