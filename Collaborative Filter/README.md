##### Collaborative Filtering


This code implements Collaborative Filter algorithm as described in paper `Empirical Analysis of Predictive Algorithms for Collaborative Filtering` referenced below.

Implementation of the Collaborative Filter is available in `CollaborativeFilter.java`. Code takes two command line arguments: a training file and a testing file. The code prints the movie, user, provided rating and prediction in a space separated format.
Results for the whole Netflix data set provided in the homework are available in `CollaborativeFilter_output.txt` file attached. Mean Absolute Error recieved was 0.6949234976496853 and Root Mean Squared Error was 0.8844601266219841.

###### Usage
```
$ javac CollaborativeFilter.java
$ java CollaborativeFilter ../data/netflix/TrainingRatings.txt ../data/netflix/TestingSample.txt  
Training file read
Movie User Rating Prediction
2660 1207170 5.0 3.6522832986846114
2866 2575071 2.0 3.2664388794755257
3274 1355423 3.0 2.9574445931998685
3418 1445521 5.0 3.947454872682519
 Absolute Error: 3.7092561149085266
 Squared Error: 4.5298699501393545
 Mean Absolute Error: 0.9273140287271316
 Root Mean Squared Error: 1.0641745568913206
```

##### Reference

Breese, John S., David Heckerman, and Carl Kadie. "Empirical analysis of predictive algorithms for collaborative filtering." Proceedings of the Fourteenth conference on Uncertainty in artificial intelligence. Morgan Kaufmann Publishers Inc., 1998.
