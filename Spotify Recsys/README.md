#### Spotify Recsys Challenge 2018

##### Problem Introduction
As part of the class project we are aiming to create a recommendation system which we could also submit for Spotify Recsys Challenge 2018. The topic of this year’s challenge is *automatic playlist continuation*. The goal of the challenge is to develop a system for the task of automatic playlist continuation. Given a set of playlist features, the developed systems shall generate a list of recommended tracks that can be added to that playlist, thereby 'continuing' the playlist. The system should also be able to cope with playlists for which no initial seed tracks are given.  
**Input**  
A user-created playlist, represented by:
* Playlist metadata
* K seed tracks: a list of the K tracks in the playlist, where K can equal 0, 1, 5, 10, 25, or 100.  

**Output**
A list of 500 recommended candidate tracks, ordered by relevance in decreasing order.

##### Tentative Approach
We plan to implement and compare the results for this problem using three approaches:
1. K Mean clustering
2. Collaborative filtering algorithms
3. K Nearest Neighbour

##### Dataset
As part of this challenge, Spotify has released the Million Playlist Dataset. It comprises a set of 1,000,000 playlists that have been created by Spotify users, and includes playlist titles, track listings and other metadata.

##### Team
This project would be done in a team of two: Mythri Thippareddy and Harsha Kokel


##### References
* J.S. Breese, D. Heckerman, C. Kadie, "Empirical Analysis of Predictive Algorithms for Collaborative Filtering", Proc. 14th Conf. Uncertainty in Artificial Intelligence, July 1998.
