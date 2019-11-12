## PS3

This code is implemented by Harsha Kokel as part of Problem set 3 during Spring 2019 for CS 6347 Probablistic Graphical Models, at The University of Texas at Dallas. It is written with python 3.6, older versions of python do not support [random.choices](https://docs.python.org/3.6/library/random.html#random.choices) and hence will not work with this code.



Code performs **Gibbs sampling** to calculate the max-marginal probability. It has two functions:
1. **gibbs**: which returns a *n* x *k* matrix of marginal values, where ith, xth entry is equal to the probability that i ∈ V is colored with color xi ∈ {1, . . . , k}.

2. **construct table**: which constructs a table of the estimated marginal as a function of **burnin** versus **its** for vertex a and color 4.

The assignment ask **'Does your answer (marginal probabilities) depend on the initial choice of assignment used in your Gibbs sampling algorithm?'** From my observations, the initial value does impact the probability when we have fewer iterations and smaller burnin samples. However, as we increase it the initial sample doesn't influence the probability values.  


Please note that the assignment of color and vertex starts from index 0, so the marginal for vertex a with color 4 is given in marginal_matrix[0,3].


### Usage

Code can be executed from **command line**


##### Gibbs

The code takes 4 mandatory arguments and one optional argument

1. `-A` Adjacency Matrix  
2. `-w` vector of weights
2. `-b` number of burnin samples
2. `-its` Number of iterations after burnin
2. `-v` verbose mode [optional]


**sample usage**

```terminal
$ python sampling.py -A "[[0, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 0]]"
 -w "[1, 2, 3, 4]" -b 20 -its 200

 [[0.16915423 0.37810945 0.35820896 0.09452736]
 [0.039801   0.039801   0.11940299 0.80099502]
 [0.02487562 0.02985075 0.11442786 0.83084577]
 [0.17910448 0.38308458 0.42288557 0.01492537]]
```


##### Construct-table

The code takes 3 mandatory arguments and one optional argument

1. `-A` Adjacency Matrix  
2. `-w` vector of weights
2. `--table`
2. `-v` verbose mode [optional]


**sample usage**
```terminal
$ python sampling.py -A "[[0, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 0]]"
 -w "[1, 2, 3, 4]" --table

['burnin', 'its', 'marginal']
[64, 64, 0.2153846153846154]
[1024, 64, 0.676923076923077]
[16384, 64, 0.4307692307692308]
[262144, 64, 0.0]
[64, 1024, 0.12878048780487805]
[1024, 1024, 0.20390243902439023]
[16384, 1024, 0.2965853658536585]
[262144, 1024, 0.34146341463414637]
[64, 16384, 0.13976197741837046]
[1024, 16384, 0.17735733902960024]
[16384, 16384, 0.18223985352456515]
[262144, 16384, 0.17430576747024717]
[64, 262144, 0.17632607907837267]
[1024, 262144, 0.17697457513971276]
[16384, 262144, 0.17460184249175076]
[262144, 262144, 0.1724541761239009]
```
