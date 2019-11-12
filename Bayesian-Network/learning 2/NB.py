import pandas as pd
import numpy as np
from math import log, inf
import logging
import argparse
from collections import defaultdict

class NaiveBayes:

    def train(self, train_file, regularization=0):
        data = pd.read_csv(train_file, header=None)
        self.classes, counts = np.unique(data.loc[:,0],return_counts=True)
        self.prior = dict(zip(self.classes, np.round( counts/np.sum(counts),4)))
        self.conditional_probability = defaultdict(lambda: {x: 1 / len(data) for x in self.classes})
        for i in range(1,len(data.columns)):
            domain = np.unique(data.loc[:,i])
            for c in self.classes:
                unique, counts = np.unique(data.loc[data[0] == c, i], return_counts=True)
                # If zero sample found for a domain
                counts = counts + 1
                missing_domain = np.setdiff1d(domain,unique)
                for m in missing_domain:
                    unique = np.append(unique, m)
                    counts = np.append(counts, regularization)
                self.conditional_probability[i][c] = defaultdict(int,zip(unique, np.round(counts/np.sum(counts),4)))

    def test_loglikelihood(self, test_file):
        data = pd.read_csv(test_file, header=None)
        correctly_predicted_examples = defaultdict(int)
        for index, row in data.iterrows():
            score = defaultdict(int)
            for c in self.classes:
                score[c] += log(self.prior[c])
                for i in range(1,len(data.columns)):
                    if self.conditional_probability[i][c][row[i]]:
                        score[c] += log(self.conditional_probability[i][c][row[i]])
                    else:
                        score[c] += -1*inf
            predicted_class = max(score, key=lambda x: score[x])
            if predicted_class == row[0]:
                correctly_predicted_examples[row[0]] += 1
        print("Correct Prediction: ", sum(correctly_predicted_examples.values()),"/",len(data))
        print("Accuracy: ", (sum(correctly_predicted_examples.values()) * 100)/len(data) )

    def test(self, test_file):
        self.test_loglikelihood(test_file)

    def test_likelihood(self, test_file):
        data = pd.read_csv(test_file, header=None)
        correctly_predicted_examples = defaultdict(int)
        for index, row in data.iterrows():
            score = defaultdict(lambda:1)
            for c in self.classes:
                score[c] *= self.prior[c]
                for i in range(1,len(data.columns)):
                    # if self.conditional_probability[i][c][row[i]]:
                    score[c] *= self.conditional_probability[i][c][row[i]]
            predicted_class = max(score, key=lambda x: score[x])
            print(index, score.values())
            if predicted_class == row[0]:
                correctly_predicted_examples[row[0]] += 1
        print("Correct Prediction: ", sum(correctly_predicted_examples.values()),"/",len(data))
        print("Accuracy: ", (sum(correctly_predicted_examples.values()) * 100)/len(data) )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="count",
                        help="increase output verbosity (e.g., -vv is more than -v)")
    parser.add_argument('-train', '--train', help='<Required> Training File', required=True)
    parser.add_argument('-test', '--test', help='<Required> Testing file', required=True)
    parser.add_argument('-reg', '--reg',  choices=['laplace', 'dirichlet'],
                        help='Use Laplace Smoothing or Dirichlet Prior')
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger("NB").setLevel(logging.DEBUG)
        logging.getLogger("NB").info("Verbose output.")
    else:
        logging.getLogger("NB").setLevel(logging.INFO)
        logging.getLogger("NB").info("Verbose output.")
        pass
    nb = NaiveBayes()
    if args.reg =='laplace':
        nb.train(args.train, 1)
    elif args.reg == 'dirichlet':
        nb.train(args.train, 0.01)
    else:
        nb.train(args.train)
    nb.test(args.test)

