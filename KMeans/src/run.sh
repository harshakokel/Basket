#!/bin/bash
for k in 2 5 10 15 20; 
do
	for i in `seq 1 10`;
	do
     		java KMeans ../img/$1.jpg $k ../output_1000/k_$k/$1_$i.jpg
	done
done 
