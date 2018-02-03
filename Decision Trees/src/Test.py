'''
Created on 02-Feb-2018

@author: hkokel
'''
from DecisionTree import DecisionTree
import sys

l_values = [10, 100, 1000, 2000, 5000]
k_values = [30, 30,  25,  10,  25]

runs = 10
entropy_heuristic_tree = DecisionTree('e')
training_set = entropy_heuristic_tree.read_data(sys.argv[1])
validation_set = entropy_heuristic_tree.read_data(sys.argv[2])
test_set = entropy_heuristic_tree.read_data(sys.argv[3])
print "=========Information Gain Heuristics starts============="
tree = entropy_heuristic_tree.learn_tree(training_set)
print "Accuracy on Test set before pruning: ", entropy_heuristic_tree.validate_data(tree, test_set)
for l, k in zip(l_values, k_values):
        print l, ",", k, 
        for i in range(0, runs):             
            new_tree = entropy_heuristic_tree.post_pruning(tree, validation_set, l, k)
            print ",", entropy_heuristic_tree.validate_data(new_tree, test_set),
            new_tree = None
        print ""
print "=========Information Gain Heuristics ends============="
print "=========Variance Impurity Heuristics starts============="
variance_heuristic_tree = DecisionTree('v')
tree = variance_heuristic_tree.learn_tree(training_set)
print "Accuracy on Test set before pruning: ", variance_heuristic_tree.validate_data(tree, test_set)
for l, k in zip(l_values, k_values):
        print l, ",", k, 
        for i in range(0, runs):             
            new_tree = variance_heuristic_tree.post_pruning(tree, validation_set, l, k)
            print ",", variance_heuristic_tree.validate_data(new_tree, test_set),
            new_tree = None
        print ""
print "=========Variance Impurity  Gain Heuristics ends============="