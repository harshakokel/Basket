# Hidden-Markov-Model

This repository contains implementation of Hidden Markov Model.

This is implemented as part of a Homework Assignment in NLP class CS 6320 in University of Texas Dallas.

It decodes best hidden sequence for a given observation sequence. The decode function implements Viterbi Algorithm.

To execute this program, use following commands:  
`python HMM.py`

User will be prompted to enter the observation sequence. Output will be the best hidden sequence and the probability of that sequence.

Sample Input:  
`123321`

Sample Output:  
`Best hidden sequence:  ['Hot', 'Hot', 'Hot', 'Hot', 'Hot', 'Cold']`  
`Prob  0.00014751744`  

The default observation set and the HMM defined in the problem is given below.

  ###### Hidden Markov Model FSA

 ![alt text](https://github.com/harshakokel/Hidden-Markov-Model/blob/master/HMM.png "Hidden Markov Model")

  ###### Hidden state set
  Q = ['Hot', 'Cold']

  ###### Initial Probability
  Pi = [0.8, 0.2 ]

  ###### Transitional Probability Matrix
  A = [[ 0.7, 0.3 ],
       [ 0.4, 0.6 ]]

  ###### Observation Likelihood
  B = [ [ 0.2, 0.5],
        [ 0.4, 0.4],
        [ 0.4, 0.1] ]

  ###### Observation Set
  O = [1, 2, 3]
