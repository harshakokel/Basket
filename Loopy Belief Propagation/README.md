## PS2

This code is implemented by Harsha Kokel as part of Problem set 2 during Spring 2019 for CS 6347 Probablistic Graphical Models, at The University of Texas at Dallas. It is written with python 3.5.

Code performs **Loopy Belief Propagation** (LBP) on the given graph for vertex coloring problem (refer PS2.pdf). Code implements two variants of LBP: sumprod and maxprod.

**Sum-product** algorithm returns the value of the partition function, it uses bethe free energy forumla to compute approximate value of *log(Z)* and **Max-product** algorithm returns return the assignment that maximizes each singleton belief for each vertex as a vector whose ith entry corresponds to the maximizing assignment of the belief for the vertex i.

Please note that the assignment of color starts from index 0, so assignment [2,2,2] is actually assigning 3rd color to each vertex.

### Usage

Code can be executed either from **command line** or from the **python console**.

#### Command line

The code takes 3 mandatory arguments and two optional argument

1. `-A` Adjacency Matrix  
2. `-w` vector of weights  
2. `-its` Number of iterations
2. `--maxprod` argument to execute maxprod algorithm to find maximizing assignments [default: sumprod ]
2. `-v` verbose mode

**Sample usage**

```terminal
$  python LBP.py -A [[0,1,0],[1,0,1],[0,1,0]] -w [0,1] -its 26
10.107337927389693
$ python LBP.py -A [[0,1,1],[1,0,1],[1,1,0]] -w [1,2,3] -its 2 --maxprod
[2, 2, 2]
```

#### Python console

The code can be imported in python console and can be executed as shown below

**Sample usage**

```console
>>> import numpy as np
>>> import LBP
>>> A = np.array([[0,1,0],[1,0,1],[0,1,0]])
>>> w = [0,1]
>>> LBP.maxprod(A,w,26)
[1, 0, 1]
>>> LBP.sumprod(A,w,24)
10.107337927389693
```
