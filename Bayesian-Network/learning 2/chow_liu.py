import pandas as pd
import numpy as np
from math import log
from scipy.sparse.csgraph import minimum_spanning_tree
import networkx as nx
from collections import defaultdict
from collections import deque
import logging
import argparse
import sys

class ChowLiu:

    def train(self, train_file, regularization=0):
        data = pd.read_csv(train_file, header=None)
        self.N = len(data)
        self.V = len(data.columns)

        self.learn_structure(data,regularization)
        self.write_structure('test.jpg')
        self.learn_parameters(data, regularization)

        # print(self.prior)
        # print(self.conditional_probability)

    def learn_parameters(self, data, regularization):
        self.classes, counts = np.unique(data.loc[:, 0], return_counts=True)
        self.prior = dict(zip(self.classes, np.round(counts / np.sum(counts), 4)))
        self.conditional_probability = dict()
        for i in range(1, len(data.columns)):
            domain = np.unique(data.loc[:, i])
            parent = list(self.structure.predecessors(i))[0]
            for p in np.unique(data.loc[:, parent]):
                unique, counts = np.unique(data.loc[data[parent] == p, i], return_counts=True)
                # If zero sample found for a
                counts = counts + regularization
                missing_domain = np.setdiff1d(domain, unique)
                for m in missing_domain:
                    unique = np.append(unique, m)
                    counts = np.append(counts, regularization)
                if i not in self.conditional_probability.keys():
                    self.conditional_probability[i] = dict()
                self.conditional_probability[i][p] = defaultdict(int, zip(unique, np.round(counts / np.sum(counts), 4)))

    def learn_structure(self, data, regularization):
        # Calculate Mutual Information of all pairs
        matrix = np.full((self.V, self.V), sys.float_info.max)
        for i in range(0, self.V):
            for j in range(i, self.V):
                if i == j:
                    continue
                mi = self.mutual_info(i, j, data)
                if mi:
                    matrix[i, j] = round(mi, 4) * -1  # To use minimum spanning tree
                    matrix[j, i] = matrix[i,j]
        # Learn structure
        mst = nx.minimum_spanning_tree(nx.from_numpy_matrix(matrix))
        # todo check for zero mutual info.
        G = nx.DiGraph()
        G.add_nodes_from(data.columns)
        queue = deque([0])
        covered = list([0])
        while len(queue):
            parent = queue.pop()
            neighbours = list(mst.neighbors(parent))
            for c in neighbours:
                if c in covered:
                    continue
                queue.append(c)
                G.add_edge(parent, c)#, weight=mst[parent, c] * -1
                covered.append(c)
        self.structure = G
        return G


    def test(self, test_file):
        data = pd.read_csv(test_file, header=None)
        correctly_predicted_examples = defaultdict(int)
        for index, row in data.iterrows():
            score = defaultdict(int)
            for c in self.classes:
                score[c] += log(self.prior[c])
                for i in range(1,len(data.columns)):
                    parent = list(self.structure.predecessors(i))[0]
                    if parent == 0 and self.conditional_probability[i][c][row[i]]:
                        score[c] += log(self.conditional_probability[i][c][row[i]])
                    elif self.conditional_probability[i][row[parent]][row[i]]:
                        score[c] += log(self.conditional_probability[i][row[parent]][row[i]])
            # print(index, score)
            predicted_class = max(score, key=lambda x: score[x])
            if predicted_class == row[0]:
                correctly_predicted_examples[row[0]] += 1
        print("Correct Prediction: ", sum(correctly_predicted_examples.values()),"/",len(data))
        print("Accuracy: ", (sum(correctly_predicted_examples.values()) * 100)/len(data) )

    def write_structure(self, filename='chow_liu.jpg'):
        p = nx.drawing.nx_pydot.to_pydot(self.structure)
        p.write_jpg(filename)

    """ 
    MI(X, Y) = \sum_{xy} P(x, y) * log [ P(x,y)/ (P(x)P(y)) ]
             = \sum_{xy} Count(x,y)/N * log [ (Count(x,y) *N )/ Count(x), Count(y)]
    """
    def mutual_info(self, node_x, node_y, data):
        regularization=0
        domain_x = np.unique(data.loc[:, node_x])
        domain_y = np.unique(data.loc[:, node_y])
        mi = 0
        for x in domain_x:
            for y in domain_y:
                c_x_y = regularization+ sum((data[node_x] == x) & ( data[node_y] == y))
                c_x = regularization + sum(data[node_x] == x)
                c_y = regularization + sum(data[node_y] == y)
                if c_x == 0 or c_y == 0 or c_x_y == 0:
                    continue
                mi +=  (c_x_y*log( (c_x_y*(self.N+(4*regularization))/(c_x*c_y)))/(self.N+(4*regularization)))
        return mi


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="count",
                        help="increase output verbosity (e.g., -vv is more than -v)")
    parser.add_argument('-train', '--train', help='<Required> Training File', required=True)
    parser.add_argument('-test', '--test', help='<Required> Testing file', required=True)
    parser.add_argument('-tree', '--write_tree', help='<Optional> filename for tree jpg', required=False)
    parser.add_argument('-reg', '--reg',  choices=['laplace', 'dirichlet'],
                        help='Use Laplace Smoothing or Dirichlet Prior')
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger("CL").setLevel(logging.DEBUG)
        logging.getLogger("CL").info("Verbose output.")
    else:
        logging.getLogger("CL").setLevel(logging.INFO)
        logging.getLogger("CL").info("Verbose output.")
        pass
    cl = ChowLiu()
    if args.reg =='laplace':
        cl.train(args.train, 1)
    elif args.reg == 'dirichlet':
        cl.train(args.train, 0.1)
    else:
        cl.train(args.train)
    cl.test(args.test)
    if args.write_tree:
        cl.write_structure(args.write_tree)