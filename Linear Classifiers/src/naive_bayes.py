import os, sys
from collections import defaultdict
from math import log
import time
from classifier import classifier

class NaiveBayes(classifier):


    def train_multinomial_nb(self, training_set):
        self.training_directory = training_set
        self.classes = [f for f in os.listdir(training_set) if not f.startswith('.')]
        self.prior = {}
        vocabulary = set()
        doc_count = defaultdict(int)
        doc_text = defaultdict(list)
        for c in self.classes:
            files_path = self.training_directory+'/'+c
            files_list = [f for f in os.listdir(files_path) if not f.startswith('.')]
            doc_count[c] += len(files_list)
            for file in files_list:
                terms = self.read_file(files_path+'/'+file)
                doc_text[c] += terms
                vocabulary = vocabulary.union(set(terms))
        self.conditional_probability = defaultdict(lambda: {x: 1/len(vocabulary) for x in self.classes })
        for c in self.classes:
            self.prior[c] = doc_count[c]/sum(doc_count.values())
            for term in vocabulary:
                self.conditional_probability[term][c] = (doc_text[c].count(term)+1)/(len(doc_text[c]) + len(vocabulary))


    def train(self, training_set):
        self.training_directory = training_set
        self.classes = [f for f in os.listdir(training_set) if not f.startswith('.')]
        self.prior = {}
        token_count = defaultdict(lambda: {x:0 for x in self.classes })
        total_count = defaultdict(int)
        for c in self.classes:
            # List all documents for the class
            files_path = self.training_directory+'/'+c
            files_list = [f for f in os.listdir(files_path) if not f.startswith('.')]
            # set only the numerator for prior probabilities
            self.prior[c] = len(files_list)
            # compute term frequency in class
            for file in files_list:
                tokens = self.read_file(files_path+'/'+file)
                total_count[c] += len(tokens)   # Total terms in class
                for token in tokens:
                    token_count[token][c] += 1
        # dividing the denominator for all priors
        total_examples = sum(self.prior.values())
        self.prior = {key_: val_/total_examples for key_, val_ in self.prior.items()}
        self.conditional_probability = defaultdict(lambda: {x: 1/len(token_count) for x in self.classes })
        for c in self.classes:
            for token in token_count:
                self.conditional_probability[token][c] = (token_count[token][c]+1)/(total_count[c]+len(token_count))

    def test(self, test_set):
        if not hasattr(self, 'prior') or len(self.prior ) == 0:
            print("Train the model before testing.")
            return
        self.test_directory = test_set
        # List of examples for the class
        no_of_examples = defaultdict(int)
        correctly_predicted_examples = defaultdict(int)
        for c in self.classes:
            files_path = self.test_directory+'/'+c
            files_list = [f for f in os.listdir(files_path) if not f.startswith('.')]
            no_of_examples[c] = len(files_list)
            for file in files_list:
                predicted_class = self.apply_multinomial_nb(files_path+'/'+file)
                if predicted_class == c:
                    correctly_predicted_examples[c] += 1
        print ("Correct Prediction: ", sum(correctly_predicted_examples.values()) ,"/", sum(no_of_examples.values()))
        print ("Accuracy: ", (sum(correctly_predicted_examples.values())*100)/sum(no_of_examples.values()))

    def apply_multinomial_nb(self, test_file_path):
        # extract all the tokens from the document
        tokens = self.read_file(test_file_path)
        # initialize score with log(prior[c])
        score = defaultdict(int)
        for c in self.classes:
            score[c] += log(self.prior[c])
            for token in tokens:
                score[c] += log(self.conditional_probability[token][c])
        return max(score, key=lambda x: score[x])
