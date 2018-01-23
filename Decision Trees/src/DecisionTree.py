"""This module implements Decision Tree."""
import numpy as np
import Tree
import math
import copy
import random
import sys


class DecisionTree:
    """This is an implementation of Decision tree learning.

    Decision tree learning provides a practical method for concept learning
    and for learning other discrete-valued functions. Algorithms infers decision
    trees by growing them from the root downward, greedily selecting the next
    best attribute for each new decision branch added to the tree. This
    implementations assumes the data (Attribute values as well as class) to be
    discrete binary integers.

    """

    def __init__(self, heuristics):
        """Initialize the decision tree with the heuristics to be used for learning."""
        self.heuristics = heuristics

    def read_data(self, filename):
        """Read CSV file."""
        data = np.recfromcsv(filename, case_sensitive=True)
        return data

    def split_data(self, data, attribute):
        """Split data. Group them by the value of attribute.

        Left returns the subset with attribute value as 0 and Right as 1.
        """
        left = list()
        right = list()
        for row in data:
            if row[attribute] == 0:
                left.append(row)
            else:
                right.append(row)
        return np.array(left, dtype=data.dtype), np.array(right, dtype=data.dtype)

    def learn_tree(self, data, visited_attribute_list=[]):
        """Learn the decision tree on the data."""
        if len(data['Class']) == 0:
            return None
        elif len(data['Class']) == sum(data['Class']):  # All instances are +ve
            return Tree.BinaryTree(1)
        elif sum(data['Class']) == 0:  # All instances are -ve
            return Tree.BinaryTree(0)
        else:
            best_attribute = self.choose_best_attribute(data, visited_attribute_list)
            if best_attribute is None:
                return None
            visited_attribute_list.append(best_attribute)
            tree = Tree.BinaryTree(best_attribute)
            tree.setPositiveExamples(sum(data['Class']))
            tree.setNegativeExamples(len(data['Class']) - sum(data['Class']))
            left_data, right_data = self.split_data(data, best_attribute)
            left_tree = self.learn_tree(left_data, list(visited_attribute_list))
            right_tree = self.learn_tree(right_data, list(visited_attribute_list))
            if left_tree is not None:
                tree.setLeftChild(left_tree)
            if right_tree is not None:
                tree.setRightChild(right_tree)
            return tree

    def choose_best_attribute(self, data, visited_attribute_list=[]):
        """Choose next best attribute to be added in decision tree."""
        visited_attribute_list.append('Class')
        attribute_list = set(x[0] for x in data.dtype.descr) - set(visited_attribute_list)
        attribute_list = list(attribute_list)
        if attribute_list is None or len(attribute_list) == 0 or len(data['Class']) == 0:
            return None
        max_gain = float('-inf')
        best_attribute = None
        for attribute in attribute_list:
            gain = self.calculate_information_gain(data, attribute)
            if gain > max_gain:
                max_gain = gain
                best_attribute = attribute
        return best_attribute

    def calculate_information_gain(self, data, attribute):
        """Calculate the information gained for given attribute."""
        current_positive = sum(data['Class'])
        current_negative = len(data['Class']) - current_positive
        gain = self.heuristics_option[self.heuristics](current_positive, current_negative)
        left, right = self.split_data(data, attribute)
        impurity_l = self.heuristics_option[self.heuristics](sum(left['Class']), len(left['Class']) - sum(left['Class']))
        impurity_r = self.heuristics_option[self.heuristics](sum(right['Class']), len(right['Class']) - sum(right['Class']))
        gain -= ((len(left['Class'])/float(len(data['Class'])))*impurity_l)
        gain -= ((len(right['Class'])/float(len(data['Class'])))*impurity_r)
        return gain

    def calculate_entropy(positive, negative):
        """Calculate entropy."""
        if positive == 0 or negative == 0:
            return 0
        pp = positive/float(negative+positive)
        pn = negative/float(negative+positive)
        H = -(pp * math.log(pp, 2)) - (pn * math.log(pn, 2))
        return H

    def calculate_variance_impurity(positive, negative):
        """Calculate variance impurity."""
        if positive == 0 or negative == 0:
            return 0
        VI = (positive/float(negative+positive))*(negative/float(negative+positive))
        return VI

    def predict_class(self, tree, row):
        """Predict the class for the row using given decision tree."""
        if tree.isLeafNode():
            return tree.getNodeValue()
        attribute = tree.getNodeValue()
        if row[attribute] == 0:
            if tree.getLeftChild():
                return self.predict_class(tree.getLeftChild(), row)
            else:
                return tree.getNodeValue()
        elif row[attribute] == 1:
            if tree.getRightChild():
                return self.predict_class(tree.getRightChild(), row)
            else:
                return tree.getNodeValue()

    def validate_data(self, tree, data):
        """Validate the accuracy of the decision tree for the given data."""
        total = len(data['Class'])
        positives = 0
        for row in data:
            if row['Class'] == self.predict_class(tree, row):
                positives += 1
        accuracy = positives/float(total)
        return accuracy

    def post_pruning(self, decision_tree, validation_set, L, K):
        """Implement post pruning algo given in HW."""
        best_tree = copy.deepcopy(decision_tree)
        current_accuracy = self.validate_data(best_tree, validation_set)
        for i in range(0, L):
            tree_prime = copy.deepcopy(best_tree)
            M = random.randint(0, K)
            for j in range(0, M):
                node_list = tree_prime.level_ordered_array()
                P = random.randint(0, len(node_list)-1)
                node = node_list[P]
                l_child = node.getLeftChild()
                r_child = node.getRightChild()
                if l_child is None or r_child is None:
                    pass
                else:
                    if l_child.getPositiveExamples() > l_child.getNegativeExamples():
                        node.setLeftChild(Tree.BinaryTree(1))
                    else:
                        node.setLeftChild(Tree.BinaryTree(0))
                    if r_child.getPositiveExamples() > r_child.getNegativeExamples():
                        node.setRightChild(Tree.BinaryTree(1))
                    else:
                        node.setRightChild(Tree.BinaryTree(0))
            new_accuracy = self.validate_data(tree_prime, validation_set)
            if new_accuracy > current_accuracy:
                best_tree = tree_prime
                current_accuracy = new_accuracy
        return best_tree

    def reduced_error_pruning(self, tree, validation_data, current_accuracy=0):
        """Prune the tree till the accuracy increases on the validation data."""
        score, prune_tree = self.prune_node(tree, tree, validation_data, tree)
        new_accuracy = self.validate_data(prune_tree, validation_data)
        if new_accuracy > current_accuracy:
            return self.prune(prune_tree, validation_data, new_accuracy)
        else:
            return tree

    def prune_node(self, root, node, validation_set, best_tree, best_score=0):
        """Prune a node from the tree rooted at root.

        Select the node which results in maximum accuracy improvement over
        validation set.
        """
        if node.left is None and node.right is None:
            return best_score, best_tree
        else:
            l_child = node.getLeftChild()
            r_child = node.getRightChild()
            best_score, best_tree = self.prune_node(root, l_child, validation_set, best_tree, best_score)
            best_score, best_tree = self.prune_node(root, r_child, validation_set, best_tree, best_score)
            if l_child.getPositiveExamples() > l_child.getNegativeExamples():
                node.setLeftChild(Tree.BinaryTree(1))
            else:
                node.setLeftChild(Tree.BinaryTree(0))
            if r_child.getPositiveExamples() > r_child.getNegativeExamples():
                node.setRightChild(Tree.BinaryTree(1))
            else:
                node.setRightChild(Tree.BinaryTree(0))
            score = self.validate_data(root, validation_set)
            if score > best_score:
                best_score = score
                best_tree = copy.deepcopy(root)
            node.setLeftChild(l_child)
            node.setRightChild(r_child)
            return best_score, best_tree

    heuristics_option = {'e': calculate_entropy,
                         'v': calculate_variance_impurity}


# Driver code
if len(sys.argv) < 7:
    print ("needs 6 arguments")
    sys.exit()
DT = DecisionTree('e')
print "===== Information Gain Heuristic starts ====="
training_set = DT.read_data(sys.argv[3])
tree = DT.learn_tree(training_set)
validation_set = DT.read_data(sys.argv[4])
new_tree = DT.post_pruning(tree, validation_set, int(sys.argv[1]), int(sys.argv[2]))
test_set = DT.read_data(sys.argv[5])
if sys.argv[6] == "yes":
    new_tree.printTree()
    print ""
print "Accuracy on Training set: ", DT.validate_data(new_tree, training_set)
print "Accuracy on Validation set: ", DT.validate_data(new_tree, validation_set)
print "Accuracy on Test set: ", DT.validate_data(new_tree, test_set)
print "===== Information Gain Heuristic ends ====="

print "===== Variance Impurity Heuristic starts ====="
DT = DecisionTree('v')
training_set = DT.read_data(sys.argv[3])
tree = DT.learn_tree(training_set)
validation_set = DT.read_data(sys.argv[4])
new_tree = DT.post_pruning(tree, validation_set, int(sys.argv[1]), int(sys.argv[2]))
test_set = DT.read_data(sys.argv[5])
if sys.argv[6] == "yes":
    new_tree.printTree()
    print ""
print "Accuracy on Training set: ", DT.validate_data(new_tree, training_set)
print "Accuracy on Validation set: ", DT.validate_data(new_tree, validation_set)
print "Accuracy on Test set: ", DT.validate_data(new_tree, test_set)
print "===== Variance Impurity Heuristic ends ====="
