from __future__ import division
from collections import defaultdict
import re
import numpy
import sys

class BigramProbabilities(object):

    unigram_c = {}
    bigram_c = {}
    bigram_p = {}
    words = 0
    vocabulary = 0
    bigram_gt = {}

    def calculateCountAndProbabilitiesFromCorpus(self, corpusfile):

        #Read the file
        file = open(corpusfile, "r")
        corpus = file.read()
        tokens = re.findall('(\S+)',corpus)
        self.words = len(tokens)

        #Calculate Unigram count
        for token in set(tokens):
            self.unigram_c[token] = tokens.count(token)
        self.vocabulary = len(self.unigram_c)

        # Calculate Bigram count and probability and write on file
        bigramList = self.createBigramList(tokens)
        file = open("BigramCountProbabilities.txt","w")
        file.write('{:<30}'.format("Bigram")+" "+'{:<5}'.format("Count")+" "+'{:<9}'.format("Probability")+"\n")
        file.write("----------------------------------------------------------\n")
        for bigram in set(bigramList):
            self.bigram_c[bigram] = bigramList.count(bigram)
            self.bigram_p[bigram] = bigramList.count(bigram)/self.unigram_c[re.findall('(\S+)', bigram)[0]]
            n = '{:<30}'.format(bigram) +" "+'{:<5}'.format(str(self.bigram_c[bigram]))+" "+'{:<9}'.format(str(self.bigram_p[bigram]))+"\n";
            file.write( n )
        file.close()

        # Calculate Add-One Smoothing Bigram count and probability and write on file
        file = open("AddOneSmoothingBigramCountProbabilities.txt","w")
        file.write('{:<30}'.format("Add-One Smoothing Bigram")+" "+'{:<12}'.format("Count")+" "+'{:<17}'.format("C* = (C+1)N/(N+V)")+" "+'{:<9}'.format("Probability")+"\n")
        file.write("--------------------------------------------------------------------------------------------------\n")
        add_one_normalizer = self.words / (self.words + self.vocabulary)
        for bigram in set(bigramList):
            n = '{:<30}'.format(bigram) +" "+'{:<12}'.format(str(self.bigram_c[bigram]))+" "+'{:<17}'.format(str(((self.bigram_c[bigram] + 1)*add_one_normalizer)))+" "+'{:<9}'.format(str((self.bigram_c[bigram] + 1)/(self.unigram_c[re.findall('(\S+)', bigram)[0]] + self.vocabulary)))+"\n";
            file.write( n )
        file.close()

        # Calculate Good Turing discounting count and probability and write on file
        self.bigram_gt = defaultdict(list)
        for key in self.bigram_c.keys():
            if self.bigram_c[key] in self.bigram_gt.keys():
                self.bigram_gt[self.bigram_c[key]].append(key)
            else:
                self.bigram_gt[self.bigram_c[key]] = [ key ]
        # print bigram_gt
        file = open("GoodTuringBigramCountProbabilities.txt","w")
        file.write('{:<8}'.format("Count")+" "+'{:<8}'.format("Nc")+" "+'{:<24}'.format("C* = (c+1)*N[c+1]/N[c]")+'{:<8}'.format("Probability")+"\n")
        file.write("--------------------------------------------------------------------------------------------------\n")
        for key in sorted(self.bigram_gt.keys()):
            gt_count = (key+1)*(len(self.bigram_gt[(key+1)])/len(self.bigram_gt[key]))
            n = '{:<8}'.format( key )+" "+'{:<9}'.format(len(self.bigram_gt[key]))+'{:<24}'.format(gt_count)+'{:<8}'.format(gt_count/self.words)+"\n";
            file.write(n)
        file.close()

    #Create bigram list
    def createBigramList(self, tokens):
        bigramList = []
        total_no_of_tokens = len(tokens)
        i = 0
        while i < total_no_of_tokens - 1:
            bigram = tokens[i] +" "+ tokens[i+1]
            bigramList.append(bigram)
            i += 1
        return bigramList

    # Bigram model without smoothing or Turing
    def bigramModel(self, bigramList):
        print ("\nSCENARIO 1: Bigram \n")
        print ('{:<30}'.format("Bigram")+" "+'{:<5}'.format("Count")+" "+'{:<9}'.format("Probability"))
        sentence_p = 1
        for bigram in bigramList:
            bigram_count, bigram_prob = 0, 0
            if bigram in self.bigram_c.keys():
                bigram_count = self.bigram_c[bigram]
            if bigram in self.bigram_p.keys():
                bigram_prob = self.bigram_p[bigram]
            sentence_p = sentence_p * bigram_prob
            print ('{:<30}'.format(bigram)+" "+'{:<5}'.format(bigram_count)+" "+'{:<9}'.format(bigram_prob))
        print( "Total bigram probability of the sentence is "+ str(sentence_p)+"\n")

    # Add One smoothing Bigram model
    def addOneSmoothingBigramModel(self, bigramList):
        print ("\nSCENARIO 2: Add-one smoothing \n")
        print ('{:<30}'.format("Bigram")+" "+'{:<5}'.format("Count")+" "+'{:<15}'.format("C*")+" "+'{:<9}'.format("Probability"))
        sentence_p = 1
        add_one_normalizer = self.words / (self.words + self.vocabulary)
        for bigram in bigramList:
            bigram_count, unigram_count = 1, 0
            if bigram in self.bigram_c.keys():
                bigram_count += self.bigram_c[bigram]
            unigram = re.findall('(\S+)', bigram)[0]
            if unigram in self.unigram_c.keys():
                unigram_count = self.unigram_c[unigram]
            bigram_prob = bigram_count/(unigram_count + self.vocabulary)
            sentence_p = sentence_p * bigram_prob
            print ('{:<30}'.format(bigram)+" "+'{:<5}'.format(bigram_count-1)+" "+'{:<15}'.format(bigram_count*add_one_normalizer)+" "+'{:<9}'.format(bigram_prob))
        print( "Total add-one smoothing bigram probability of the sentence is "+ str(sentence_p)+"\n")

    # Good Turing Discounting Bigram model
    def goodTuringBigramModel(self, bigramList):
        print ("\nSCENARIO 3: Good-Turing discounting \n")
        print ('{:<30}'.format("Bigram")+" "+'{:<5}'.format("Count")+" "+'{:<15}'.format("C*")+" "+'{:<9}'.format("Probability"))
        sentence_p = 1
        for bigram in bigramList:
            bigram_count = 0;
            if bigram in self.bigram_c.keys():
                bigram_count += self.bigram_c[bigram]
            if bigram_count == 0:
                gt_count = len(self.bigram_gt[1])
            else:
                gt_count = (bigram_count+1)*(len(self.bigram_gt[(bigram_count+1)])/len(self.bigram_gt[bigram_count]))
            sentence_p = sentence_p * (gt_count/self.words)
            print ('{:<30}'.format(bigram)+" "+'{:<5}'.format(bigram_count)+" "+'{:<15}'.format(gt_count)+" "+'{:<9}'.format(gt_count/self.words))
        print( "Total good turing discounting bigram probability of the sentence is "+ str(sentence_p)+"\n")

    def format_matrix(self, header, matrix):
        top_format = '{:^{}}'
        left_format = '{:<{}}'
        cell_format = '{:>{}.6f}'
        row_delim = '\n'
        col_delim = ' | '
        table = [[''] + header] + [[name] + row for name, row in zip(header, matrix)]
        table_format = [['{:^{}}'] + len(header) * [top_format]] \
                     + len(matrix) * [[left_format] + len(header) * [cell_format]]
        col_widths = [max(len(format.format(cell, 0))
                          for format, cell in zip(col_format, col))

                      for col_format, col in zip(zip(*table_format), zip(*table))]
        return row_delim.join(
               col_delim.join(
                   format.format(cell, width)
                   for format, cell, width in zip(row_format, row, col_widths))
               for row_format, row in zip(table_format, table))

#Driver code
b = BigramProbabilities()
if len(sys.argv) < 2:
    print ("CORPUS MISSING")
    sys.exit()
print ("Please wait till prompted!\n")
b.calculateCountAndProbabilitiesFromCorpus(sys.argv[1])
while True:
    print ("Enter the sentence or type 'q' to exit")
    sentence = raw_input()
    if sentence == "q":
        break
    tokens = re.findall('(\S+)',sentence)
    bigramList = b.createBigramList(tokens)
    b.bigramModel(bigramList)
    b.addOneSmoothingBigramModel(bigramList)
    b.goodTuringBigramModel(bigramList)
print ("\nExiting the program\n")
