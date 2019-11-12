## PS4

This code is implemented by Harsha Kokel as part of Problem set 4 during Spring 2019 for CS 6347 Probablistic Graphical Models, at The University of Texas at Dallas. It is written with python 3.6.

Code performs maximum likelihood parameter estimation to figure out the weights of each color assignment for a vertex coloring problem from the adjacency matrix of a graph and samples of observed variables (refer PS4.pdf). Code implements two variants of parameter estimation: **Gradient Ascent** (`colormle`) and **Expectation Maximization** (`colorem`)

Please note that the assignment of color starts from index 1 by default as asked by Prof. on Piazza. So, a weight [10,3,4] implies weight 10 for color 1. However, if samples have an assignment of color 0, then algorithm assumes color assignments start from 0. As my examples were not converging I have limited the number of iterations by default to 50, this can be changed by its parameter below.

#### Usage

Code can be executed either from **command line** or from the **python console**.

#### Command line

Command line execution takes the original weights, generates the samples using gibbs sampling, and then estimates the weights from the samples. The code takes 4 mandatory arguments and 3 optional argument

1. `-A` Adjacency Matrix  
2. `-w` vector of weights  
2. `-b` burnin samples
2. `-s` Number of samples
2. `-its` Number of iterations
2. `-L` vector of latent variables  [Mandatory in case of --em]
2. `--em` argument to use colorem algorithm  [default: colormle ]
2. `-v` verbose mode

**Sample usage**

```terminal
$ python mle.py -A [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,0,1]]
-w [4,10,2,8,1] -b 100 -s 10000
[ 5.03774323 14.66237689  1.34772997 13.01716998  1.        ]
$ python mle.py -A [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,0,1]]
-L [0,1,0,0] -w [4,10,2,8,1] -b 100 -s 100 --em
[ 3.08014516 15.41843636  1.10273008  3.6482942   0.55039419]
```

#### Python console

The code can be imported in python console and can be executed as shown below

**Sample usage**

```console
>>> import numpy as np
>>> import mle
>>> its = 200
>>> A = np.array([[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,0,1]])
>>> samples
>>> w1 = mle.colormle(A,samples)
>>> w2 = mle.colormle(A,samples, its)
>>> L = [0,1,0,0]
>>> w3 = mle.colorem(A,L,samples)
>>> w4 = mle.colorem(A,L,samples, its)
```


**Gradient Derivations are also attached**