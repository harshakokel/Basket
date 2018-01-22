"""This module implements Decision Tree."""
import random
import numpy as np
import Tree

class DecisionTree:
    """This is an implementation of Decision tree learning.

    Decision tree learning provides a practical method for concept learning
    and for learning other discrete-valued functions. Algorithms infers decision
    trees by growing them from the root downward, greedily selecting the next
    best attribute for each new decision branch added to the tree. This
    implementations assumes the data (Attribute values as well as class) to be
    discrete binary integers.


    """
    def read_data(self, filename):
        """Read CSV file."""
        data = np.recfromcsv(filename, case_sensitive=True)
        return data

    def split_data(self, data, attribute):
        """Split data. Group them by the value of attribute.

        Left returns the subset with attribute value as 0 and Right as 1.
        """
        left = list()
        left_p = 0
        right = list()
        right_p = 0
        for row in data:
            if row[attribute] == 0:
                left.append(row)
                if row['Class']:
                    left_p += 1
            else:
                right.append(row)
                if row['Class']:
                    right_p += 1
        return np.array(left, dtype=data.dtype), left_p, np.array(right, dtype=data.dtype), right_p

    def learn_tree(self, data, visited_attribute_list):
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
            print 'best attribute recieved: ', best_attribute
            visited_attribute_list.append(best_attribute)
            tree = Tree.BinaryTree(best_attribute)
            left_data, left_p, right_data, right_p = self.split_data(data, best_attribute)
            left_tree = self.learn_tree(left_data, visited_attribute_list)
            right_tree = self.learn_tree(right_data, visited_attribute_list)
            if left_tree is not None:
                tree.setLeftChild(left_tree)
            if right_tree is not None:
                tree.setRightChild(right_tree)
            return tree

    def choose_best_attribute(self, data, visited_attribute_list):
        visited_attribute_list.append('Class')
        attribute_list = set(x[0] for x in data.dtype.descr) - set(visited_attribute_list)
        if len(attribute_list) == 0:
            return None
        # print attribute_list
        return random.choice(list(attribute_list))        


# Driver code
DT = DecisionTree()
data = DT.read_data('../data/play_set.csv')
tree = DT.learn_tree(data, [])
tree.printTree(0)
# a, b, c, d = DT.split_data(data, 'XG')
# print len(a), b, len(c), d
