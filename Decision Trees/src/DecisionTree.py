"""This module implements Decision Tree."""
import numpy as np
import Tree
import math


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
            return self.predict_class(tree.getLeftChild(), row)
        elif row[attribute] == 1:
            return self.predict_class(tree.getRightChild(), row)

    def validate_data(self, tree, data):
        """Validate the accuracy of the decision tree for the given data."""
        total = len(data['Class'])
        positives = 0
        for row in data:
            if row['Class'] == self.predict_class(tree, row):
                positives += 1
        accuracy = positives/float(total)
        return accuracy

    heuristics_option = {'e': calculate_entropy,
                         'v': calculate_variance_impurity}


# Driver code
DT = DecisionTree('e')
training_set = DT.read_data('../data/data_sets1/training_set.csv')
tree = DT.learn_tree(training_set)
tree.printTree()
validation_set = DT.read_data('../data/data_sets1/validation_set.csv')
test_set = DT.read_data('../data/data_sets1/test_set.csv')
print ""
print "Accuracy of Validation set: ", DT.validate_data(tree, validation_set)
print "Accuracy of Test set: ", DT.validate_data(tree, test_set)
