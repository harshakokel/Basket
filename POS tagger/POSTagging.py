from __future__ import print_function
from collections import defaultdict
import sys
import re
import json

class POSTagging(object):

    unigram_model = {}
    transformation_rule = {}
    threshold = 50
    corpus_tag = []
    s_u_tag = []
    s_b_tag = []

    def createUnigramModel(self, corpusfile):
        #Read the file
        file = open(corpusfile, "r")
        corpus = file.read()
        tokens = re.findall('(\S+)',corpus)
        words = len(tokens)

        #Unigram POS tag list
        unigram_pos_list = defaultdict(list)
        for token in tokens:
            unigram = re.split("_",token)
            unigram_pos_list[unigram[0]].append(unigram[1])
        file = open("UnigramModelPOSTagging.txt","w")
        file.write('{:<20}'.format("Unigram")+" "+'{:<5}'.format("Most probable tag")+"\n")
        file.write("----------------------------------------------------------\n")
        self.unigram_model = defaultdict(str)
        for unigram in unigram_pos_list.keys():
            tag = max(unigram_pos_list[unigram],key=unigram_pos_list[unigram].count)
            self.unigram_model[unigram] = tag
            file.write('{:<20}'.format(unigram)+" "+'{:<5}'.format(tag)+"\n")
        file.close()

        #Create corpus tag
        i = 0
        for token in tokens:
            # print (re.split("_",token)[0], " ", self.unigram_model[re.split("_",token)[0]])
            self.corpus_tag.append(self.unigram_model[re.split("_",token)[0]])
            i += 1

    def generateTransformationRules(self, corpusfile):
        #From: Prev : To: (Fixed, broken, Score)
        self.transformation_rule = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda: [0]*3)))
        file = open(corpusfile, "r")
        wc = 0;
        # for line in file:
        tokens = re.findall('(\S+)',file.read())

        #Generate Transformation rules
        i = 0;
        while i < len(tokens):
            if i == 0:
                i += 1
                wc += 1
                continue
            unigram = re.split("_",tokens[i])
            if unigram[1] != self.corpus_tag[wc]:
                fr = self.corpus_tag[wc]
                to = unigram[1]
                prev = re.split("_",tokens[i])[1]
                self.calculateScoreForTransformationRule(fr, to, prev, corpusfile)
            i += 1
            wc += 1
        file = open("TransformationRulesPOSTagging.txt","w")
        file.write('{:<6}'.format("From")+" "+'{:<6}'.format("To")+" "+'{:<10}'.format("Previous")+" "+'{:<6}'.format("Fixed")+" "+'{:<6}'.format("Broken")+" "+'{:<6}'.format("Score")+"\n")
        file.write("----------------------------------------------------------\n")
        for f in self.transformation_rule.keys():
            for p in self.transformation_rule[f].keys():
                for t in self.transformation_rule[f][p].keys():
                    file.write('{:<6}'.format(f)+" "+'{:<6}'.format(t)+" "+'{:<10}'.format(p)+" "+'{:<6}'.format(self.transformation_rule[f][p][t][0])+" "+'{:<6}'.format(self.transformation_rule[f][p][t][1])+" "+'{:<6}'.format(self.transformation_rule[f][p][t][2])+"\n")
        file.close()

    def calculateScoreForTransformationRule(self,fr, to, prev, corpusfile):
        wc = 0
        fixed = 0
        broken = 0
        # if self.transformation_rule[fr][prev][to][2] == 0:
        file = open(corpusfile, "r")
        for line in file:
            tokens = re.findall('(\S+)',line)
            i = 0;
            while i < len(tokens):
                if i==0:
                    wc += 1
                    i += 1
                    continue
                if self.corpus_tag[wc] == fr and self.corpus_tag[wc-1] == prev:
                    unigram = re.split("_",tokens[i])
                    if unigram[1] == to:
                        fixed += 1
                    else:
                        broken += 1
                wc += 1
                i += 1
        self.transformation_rule[fr][prev][to][0] = fixed
        self.transformation_rule[fr][prev][to][1] = broken
        self.transformation_rule[fr][prev][to][2] = self.transformation_rule[fr][prev][to][0] - self.transformation_rule[fr][prev][to][1]
        if fixed > broken:
            #apply rules
            i = 0
            wc = 0
            for line in file:
                tokens = re.findall('(\S+)',line)
                i = 0;
                while i < len(tokens):
                    if i==0:
                        wc += 1
                        i += 1
                        continue
                    if self.corpus_tag[wc] == fr and self.corpus_tag[wc-1] == prev:
                        self.corpus_tag[wc] = to
                    wc += 1
                    i += 1
            # print ( fr, to, prev)

    def tagSentence(self,sentence):
        tokens = re.findall('(\S+)',sentence)

        #Unigram & Brill Model Tags
        tag = []
        brill = []
        i = 0
        while i < len(tokens):
            # print i
            f = self.unigram_model[tokens[i]]
            tag.append(f)
            if i == 0:
                brill.append(f)
                i+= 1
                continue
            rules = self.transformation_rule[f][tag[i-1]]
            for to in rules.keys():
                if rules[to][2] > 0:
                    f = to
                    break
            brill.append(f)
            i += 1
        print ('{:<10}'.format("Sentence"), end='')
        print (tokens)
        print ('{:<10}'.format("Unigram"), end='')
        print (tag)
        print ('{:<10}'.format("Brill"), end='')
        print (brill)
        self.s_u_tag = tag
        self.s_b_tag = brill

    def calculateError(self, sentence):
        tokens = re.findall('(\S+)',sentence)
        i = 0
        u_error = 0
        b_error = 0
        while i < len(tokens):
            unigram = re.split("_",tokens[i])
            # print (unigram[1], self.s_u_tag[i], self.s_b_tag[i] )
            if unigram[1] != self.s_u_tag[i]:
                u_error += 1
            if unigram[1] != self.s_b_tag[i]:
                b_error += 1
            i += 1
        # print (u_error)
        error_u = float(u_error)/len(tokens)
        # print  (error_u)
        # print (b_error)
        error_b = float(b_error)/len(tokens)
        # print (error_b)
        print ("Error for unigram model : ", '{:<10}'.format(error_u),"\n")
        print ("Error for brills model : ", '{:<10}'.format(error_b),"\n")

#Driver code
if len(sys.argv) < 2:
    print ("CORPUS MISSING")
    sys.exit()
print ("Please wait till prompted!\n")
p = POSTagging()
p.createUnigramModel(sys.argv[1])
p.generateTransformationRules(sys.argv[1])
while True:
    print ("Enter the sentence or type 'q' to exit")
    sentence = raw_input()
    if sentence == "q":
        break
    p.tagSentence(sentence)
    print ("Enter the sentence with POS TAG")
    pos_sentence = raw_input()
    p.calculateError(pos_sentence)
