import os, sys
import numpy as np
from classifier import classifier
from numpy import random

class Perceptron(classifier):
    x0 = "BIAS-X0"
    label = "CLASS-LABEL"
    learning_rate = 0.005
    
    def train_and_learn(self, training_set):
        print("Reading training data: ", training_set)
        # Get Classes from the training set
        training_directory = training_set
        self.classes = [f for f in os.listdir(training_set) if not f.startswith('.')]
        
        # Get List of files and Split Training and Validation set
        files_list = []
        train_files_list = []
        validation_files_list = []
        
        for c in self.classes:
            files_path = training_directory+'/'+c
            temp = [training_directory+'/'+c+'/'+f for f in os.listdir(files_path) if not f.startswith('.')]
            train, validation = self.split(temp)
            files_list += temp
            train_files_list  += train
            validation_files_list += validation 
        
        #Shuffle training & Validation
        random.shuffle(train_files_list)
        random.shuffle(validation_files_list)
        
        # Create Vocabulary
        vocabulary = set() 
        for file in files_list:
            terms = self.read_file(file)
            vocabulary = vocabulary.union(set(terms))
        
            
        # Create X matrix  (Training and Validation)   
        d_type = [(self.x0, 'float64')] + [(x,'float64') for x in vocabulary] + [(self.label,'float64')]
        train_matrix = np.zeros(len(train_files_list), dtype=d_type)
        val_matrix = np.zeros(len(validation_files_list), dtype=d_type)
        
        # assign Set-Of-Word model of each file to matrix X (all Training samples)
        count = 0
        for file in train_files_list:
            terms = self.read_file(file)
            for term in terms:
                train_matrix[count][term] = 1
            train_matrix[count][self.x0] = 1
            # assign label
            if training_set+'/'+self.classes[0] in file:
                train_matrix[count][self.label] = -1
            elif training_set+'/'+self.classes[1] in file:
                train_matrix[count][self.label] = 1
            else:
                print ("Random file")
            count += 1
        
        # assign Set-Of-Word model of each file to matrix X (all Validation samples)
        count = 0
        for file in validation_files_list:
            terms = self.read_file(file)
            for term in terms:
                val_matrix[count][term] = 1
            val_matrix[count][self.x0] = 1
            # assign label
            if training_set+'/'+self.classes[0] in file:
                val_matrix[count][self.label] = -1
            elif training_set+'/'+self.classes[1] in file:
                val_matrix[count][self.label] = 1
            else:
                print ("Random file")
            count += 1
        
        
        # possible values of learning_rate
        
        best_accuracy = float('-inf')
        best_iteration = 0
            
        # Initialize weights to 0
        self.weights = {x:0 for x in vocabulary }
        self.weights[self.x0] = 0
        
        print ("Learning begins")
        misclassified = True # False when all examples are classified correctly
        count = 0
        while misclassified:
            misclassified = False
            count += 1
            print ("iteration", count)
            for X in train_matrix:
                weights_updated = self.train_rule(X)
                if weights_updated:
                    misclassified = True
            accuracy = self.validate(val_matrix)
            if accuracy >= best_accuracy:
                best_accuracy = accuracy
                best_iteration = count
            if count > 50: #Hard condition
                break
        print ("Best accuracy", best_accuracy)
        print ("Best Iteration", best_iteration)
        print ("Learning ends")
        self.train (training_set, best_iteration)
        
        
    def train(self, training_set, iteration):
        self.no_of_iterations = iteration

        # Get Classes from the training set
        training_directory = training_set
        self.classes = [f for f in os.listdir(training_set) if not f.startswith('.')]
        
        # Get List of files
        files_list = []
        for c in self.classes:
            files_path = training_directory+'/'+c
            files_list += [training_directory+'/'+c+'/'+f for f in os.listdir(files_path) if not f.startswith('.')]
            
        
        random.shuffle(files_list)
        
        # Create Vocabulary
        vocabulary = set() 
        for file in files_list:
            terms = self.read_file(file)
            vocabulary = vocabulary.union(set(terms))
        
        # Create X matrix  (Training and Validation)   
        d_type = [(self.x0, 'float64')] + [(x,'float64') for x in vocabulary] + [(self.label,'float64')]
        X_matrix = np.zeros(len(files_list), dtype=d_type)
        
        # assign Set-Of-Word model of each file to matrix X (all Training samples)
        count = 0
        for file in files_list:
            terms = self.read_file(file)
            for term in terms:
                X_matrix[count][term] = 1
            X_matrix[count][self.x0] = 1
            # assign label
            if training_set+'/'+self.classes[0] in file:
                X_matrix[count][self.label] = -1
            elif training_set+'/'+self.classes[1] in file:
                X_matrix[count][self.label] = 1
            else:
                print ("Random file")
            count += 1
        
        # Initialize weights to 0
        self.weights = {x:0 for x in vocabulary }
        self.weights[self.x0] = 0
        
        print ("Training begins")
        # For iterations
        for i in range(0, self.no_of_iterations):
            print("Training iteration: ", i)
            for X in X_matrix:
                self.train_rule(X)
        print ("Training ends")
            
    def validate(self, val_matrix):
        correct_classification = 0
        for sample in val_matrix:
            prediction = self.predict(sample)
            expectation = sample[self.label]
            if prediction == expectation:
                correct_classification += 1
        print ("Correct Prediction: ", correct_classification,"/", len(val_matrix))
        print ("Accuracy: ", (correct_classification*100)/len(val_matrix))
        return correct_classification
    
    def split(self, files_list):
        '''Splits training data into 70/30 ratio of training and validation'''
        train_files_list = files_list[:round(len(files_list)*0.70)]
        validation_files_list = files_list[round(len(files_list)*0.70):]
        return train_files_list, validation_files_list          
    
    def train_rule(self, X):
        prediction = self.predict(X)
        label = X[self.label]
        if prediction != label:
            # Update weights
            updated_weights = {w:0 for w in self.weights }
            for i in self.weights:
                # W(t+1) = W(t) + alpha*(t-o)*X
                updated_weights[i] = self.weights[i] + (self.learning_rate*(label-prediction)*X[i])
            self.weights = updated_weights
            prediction = self.predict(X)
            if prediction != label:
                print("Error in learning")
                sys.exit() 
            return True 
        return False
        
    def sign(self, z):
        if z > 0:
            return 1
        else:
            return -1
    
    def predict(self, X):
        z = 0
        for i in self.weights:
            z += X[i]* self.weights[i]
        return self.sign(z)
    
    def test_example(self, test_example):
        # Create X matrix   
        d_type = [(x,'float64') for x in self.weights]
        X_matrix = np.zeros(1, dtype=d_type)
        terms = self.read_file(test_example)
        for term in terms:
            if term in X_matrix.dtype.names: 
                X_matrix[0][term] = 1
        X_matrix[0][self.x0] = 1
        prediction = self.predict(X_matrix[0])  
        if prediction == -1:
            return self.classes[0]
        elif prediction == 1:
            return self.classes[1]
        else:
            return "Error"
            
    def test(self, test_set):
        print ("Reading testing data: ", test_set)
        # Get List of files
        testing_directory = test_set        
        files_list = []
        for c in self.classes:
            files_path = testing_directory+'/'+c
            files_list += [testing_directory+'/'+c+'/'+f for f in os.listdir(files_path) if not f.startswith('.')]
       
        # Create X matrix   
        d_type = [(x,'float64') for x in self.weights] + [(self.label,'float64')]
        X_matrix = np.zeros(len(files_list), dtype=d_type)
        
        # assign Set-Of-Word model of each file to matrix X (all Training samples)
        count = 0
        for file in files_list:
            terms = self.read_file(file)
            for term in terms:
                if term in X_matrix.dtype.names: 
                    X_matrix[count][term] = 1
            X_matrix[count][self.x0] = 1
            # assign label
            if testing_directory+'/'+self.classes[0] in file:
                X_matrix[count][self.label] = -1
            elif testing_directory+'/'+self.classes[1] in file:
                X_matrix[count][self.label] = 1
            else:
                print ("Random file")
            count += 1
        
        print ("Testing begins")
        self.validate(X_matrix)
        print ("Testing ends")
            
    
