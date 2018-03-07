# Decision Tree 

This code is implemented as part of Homework 1 in CS 6375 Machine Learning Course at The University of Texas at Dallas. It is written with python 2.7.

Decision tree learning provides a practical method for concept learning and for learning other discrete-valued functions. Algorithms infers decision trees by growing them from the root downward, greedily selecting the next best attribute for each new decision branch added to the tree. 
    
This assignment was to implement Decision Tree Learning algorithm. This was divided into two parts. First part was learning the tree from training set and second part was pruning the tree based on validation set. The data set used for this development is available [here](http://www.hlt.utdallas.edu/~vgogate/ml/2018s/homeworks.html). Each data set is divided into three sets: the training set, the validation set and the test set. Data sets are in CSV format. The first line in the file gives the attribute names. Each line after that is a training (or test) example that contains a list of attribute values separated by a comma. The last attribute is the class-variable. Assume that all attributes taken values from the domain {0,1}.

##### Learning Tree
The following two heuristics are implemented for selecting the next attribute:

1. Information gain heuristic (mentioned in [Mitchell, Tom M.](http://www.cs.cmu.edu/~tom/) (1997) [Machine Learning](https://www.cs.cmu.edu/~tom/mlbook.html))
2. Variance impurity heuristic described below.  
Let K denote the number of examples in the training set. Let K0 denote the number of training examples that have class = 0 and K1 denote the number of training examples that have class = 1. The variance impurity of the training set S is defined as

 ![alt text](https://github.com/harshakokel/Machine-Learning/blob/master/Assets/variance-impurity-equation.png "Variance Impurity equation")

Notice that the impurity is 0 when the data is pure. The gain for this impurity is defined as usual

 ![alt text](https://github.com/harshakokel/Machine-Learning/blob/master/Assets/information-gain-equation.png "Information Gain equation")

where X is an attribute, Sx denotes the set of training examples that have X = x and Pr(x) is the fraction of the training examples that have X = x (i.e., the number of training examples that have X = x divided by the number of training examples in S).

##### Pruning Tree
Implement Post Pruning algorithm as given below.

 ![alt text](https://github.com/harshakokel/Machine-Learning/blob/master/Assets/post-pruning-algo.png "Post Pruning Algorithm")
 
#### Usage

The code takes 6 arguments

python DecisionTree.py &lt;L&gt; &lt;K&gt; &lt;training-set&gt; &lt;validation-set&gt; &lt;test-set&gt; &lt;to-print&gt;    

**L**: integer (used in the post-pruning algorithm)    
**K**: integer (used in the post-pruning algorithm)  
**training-set**: path to training csv  
**validation-set**: path to validation csv  
**test-set**: path to test csv  
**to-print**: {yes,no}    

Sample run:  

```python
$python DecisionTree.py 100 10 ./data/data_sets2/training_set.csv ./data/data_sets2/validation_set.csv ./data/data_sets2/test_set.csv no

===== Information Gain Heuristic starts =====
Accuracy on Test set before pruning:  74.5
Accuracy on Test set after pruning:  76.0
===== Information Gain Heuristic ends =====

===== Variance Impurity Heuristic starts =====
Accuracy on Test set before pruning:  74.5
Accuracy on Test set after pruning:  78.3333333333
===== Variance Impurity Heuristic ends =====
```

if to-print is set to **yes**, post-pruned tree will be printed right before the **Accuracy on Test set before pruning**

##### Tree Format
The decision tree is printed in output if the to-print parameter is set to **yes**. The format of the tree is as follows:

```shell
wesley = 0 :  
| honor = 0 :  
| | barclay = 0 : 1  
| | barclay = 1 : 0  
| honor = 1 :  
| | tea = 0 : 0  
| | tea = 1 : 1  
wesley = 1 : 0  
```

According to this tree, if wesley = 0 and honor = 0 and barclay = 0, then the class value of the corresponding instance should be 1. In other words, the value appearing before a colon is an attribute value, and the value appearing after a colon is a class value.


