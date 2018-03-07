import numpy as np
from classifier import classifier
from math import exp, log

class LogisticRegression(classifier):
    x0 = "BIAS-X0"
    label = "CLASS-LABEL"
    no_of_iterations = 10
    learning_rate = 0.05

    def train_and_learn(self, training_set, lambda_candidates):

        print("Reading training data ", training_set)
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
                train_matrix[count][self.label] = 0
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
                val_matrix[count][self.label] = 0
            elif training_set+'/'+self.classes[1] in file:
                val_matrix[count][self.label] = 1
            else:
                print ("Random file")
            count += 1

        best_lambda = 0
        best_loglikelihood = float('-inf')
        print ("Learning begins")

        for l in lambda_candidates:
            self.lambda_value = l
            print ("Lambda: ", self.lambda_value)

            # Initialize weights to 0
            self.weights = {x:0 for x in vocabulary }
            self.weights[self.x0] = 0

            # For iterations
            for i in range(0, self.no_of_iterations):
                self.gradient_descent(train_matrix)
            loglikelihood = self.validate(val_matrix)
            if loglikelihood > best_loglikelihood:
                best_lambda = self.lambda_value
                best_loglikelihood = loglikelihood
        print ("Best Lambda", best_lambda)
        print ("Best Log Likelihood", best_loglikelihood)

        print ("Learning ends")
        self.train(training_set, best_lambda)


    def train(self, training_set, lambda_value):
        self.lambda_value = lambda_value
        # Get Classes from the training set
        training_directory = training_set
        self.classes = [f for f in os.listdir(training_set) if not f.startswith('.')]

        # Get List of files
        files_list = []
        for c in self.classes:
            files_path = training_directory+'/'+c
            files_list = [training_directory+'/'+c+'/'+f for f in os.listdir(files_path) if not f.startswith('.')]

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
                X_matrix[count][self.label] = 0
            elif training_set+'/'+self.classes[1] in file:
                X_matrix[count][self.label] = 1
            else:
                print ("Random file")
            count += 1

        # Initialize weights to 0
        self.weights = {x:0 for x in vocabulary }
        self.weights[self.x0] = 0

        # For iterations
        for i in range(0, self.no_of_iterations):
            self.gradient_descent(X_matrix)

    def validate(self, val_matrix):
            likelihood = 0
            correct_classification = 0
            for sample in val_matrix:
                prediction_0 = self.predict_0(sample)
                prediction_1 = self.predict_1(sample)
                expectation = sample[self.label]
                likelihood += (expectation*log(prediction_1)) + ((1-expectation)*log(prediction_0))
                if prediction_0 > prediction_1 and expectation == 0:
                    correct_classification += 1
                elif prediction_1 > prediction_0 and expectation == 1:
                    correct_classification += 1
            mod_w = np.linalg.norm(list(self.weights.values()))
            log_likelihood = likelihood - (self.lambda_value* mod_w * mod_w /2)
            print ("lambda ", self.lambda_value)
            print ("learning rate: ", self.learning_rate)
            print ("Prediction: ", correct_classification,"/", len(val_matrix))
            print ("Accuracy: ", (correct_classification*100)/len(val_matrix))
#             print ("log likelihood: ", log_likelihood)
            return (correct_classification*100)/len(val_matrix)

    def split(self, files_list):
        '''Splits training data into 70/30 ratio of training and validation'''
#         random.shuffle(files_list)
        train_files_list = files_list[:round(len(files_list)*0.70)]
        validation_files_list = files_list[round(len(files_list)*0.70):]
        return train_files_list, validation_files_list

    def gradient_descent(self, examples):
        # Predict all the training examples
        predictions = []
        for X in examples:
                prediction_1 = self.predict_1(X)
                predictions.append(prediction_1)

        # Update weights
        updated_weights = {w:0 for w in self.weights }
        for i in self.weights:
            temp = 0
            # Calculating sum over all samples for current feature
            for l in range(0, len(predictions)):
                #  Sigma(X*(Expected - Predicted))
                temp += (examples[l][i]* (examples[l][self.label] - predictions[l]))
            # W(t+1) = W(t) + alpha*Sum_over_samples(X*(Expected - Predicted)) - alpha*lambda*W(t)
            updated_weights[i] = self.weights[i] + (self.learning_rate*temp) - (self.learning_rate*self.lambda_value*self.weights[i] )
        self.weights = updated_weights

    def sigmoid(self, z):
        try:
            return 1/(1+exp( -1* z))
        except OverflowError:
            print ("overflow")
            return 0 # If z overflows return 1/1+exp(700)

    def predict_1(self, X):
        z = self.dot_product(X)
        return 1/(1+exp(-1*z))

    def predict_0(self, X):
        z = self.dot_product(X)
        return 1/(1+exp(z))

    def dot_product(self, X):
        z = 0
        for i in self.weights:
            z += X[i]* self.weights[i]
        return z

    def test(self, test_set):
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
                X_matrix[count][self.label] = 0
            elif testing_directory+'/'+self.classes[1] in file:
                X_matrix[count][self.label] = 1
            else:
                print ("Random file")
            count += 1
        self.validate(X_matrix)
