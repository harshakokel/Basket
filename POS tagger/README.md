# CS6320-POS-TAGGER
This Homework 2 of CS 6320 taken in Fall'17

The coding is done in python  

Q1  
BigramProbabilities.py contains Q1.
Sample code to run the q1 is given below:  
```python
python BigramProbabilities.py ./HW2_F17_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Unix.txt
```

Only the corpus will be taken as the arguement.
The Following files will be generated for whole corpus:  
  BigramCountProbabilities.txt  
  AddOneSmoothingBigramCountProbabilities.txt  
  GoodTuringBigramCountProbabilities.txt  

Once the corpus is computed the user will be prompted to input the sentence.
Code will print the bigram, count, probability & total probability for all three Scenarios simultaneously.

use 'q' to exit.


Q2:

Find one tagging error in each of the following sentences that are tagged with the Penn Treebank POS tagset:  
(Theory question, error found manually)

1. I/PRP need/VBP a/DT flight/NN from/IN Atlanta/NN  
Atlanta -> NNP
2. Does/VBZ this/DT flight/NN serve/VB dinner/NNS  
dinner -> NN
3. I/PRP have/VB a/DT friend/NN living/VBG in/IN Denver/NNP  
have -> VBP
4. Can/VBP you/PRP list/VB the/DT nonstop/JJ afternoon/NN   flights/NNS
Can -> MD

Q3:  
POSTagging.py contains Q3.
Sample code to run q3 is given below:
```
python POSTagging.py HW2_F17_NLP6320_POSTaggedTrainingSet-Unix.txt
```

First the Corpus will be read and unigram model will be generated  
UnigramModelPOSTagging.txt  
TransformationRulesPOSTagging.txt  

Transformation Rules generated will be available in the TransformationRulesPOSTagging.txt file.

Then the user will be prompted on console to input the sentence.
sample input:
```
The president wants to control the board 's control
```

Code will print the TAGs derived from unigram model and the Brill tagger.
Then it will prompt for sentence with POS tag.
sample input:

```
The_DT president_NN wants_VBZ to_TO control_VB the_DT board_NN 's_POS control_NN
```

Then the code will calculate and display the Error rate for unigram model as well as POS tagger.
