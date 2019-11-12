# Word Sense Disambiguation

This implementation was done as part of programming assignment in CS 6320 Natural Language Processing in Fall 2017 by Harsha Kokel.

Every word can have multiple senses associated with it. These senses are easily available in the WordNet or any dictionary.
Word Sense Disambiguation (WSD) is the task of selecting the correct sense for a word in the given context. There are multiple ways to disambiguate the word sense. One of them is **SIMPLIFIED LESK** algorithm, which is implemented here.

### USAGE

To disambiguate a word in a sentence, import the SimplifiedLesk.py and call disambiguate function. Sample code run is shown below.

```python
$ python
>>> import SimplifiedLesk as sl
>>> lesk = sl.SimplifiedLesk()
>>> word = “deposits”
>>> sentence = “The bank can guarantee deposits will eventually cover future tuition costs because it invests in adjustable-rate mortgage securities.”
>>> sense = lesk.disambiguate(word, sentence)
>>> sense.definition()
u'money deposited in a bank or some similar institution'
```

### SETUP

This implementation uses NLTK stopwords, wordnet and word_tokenizer with python3.

If you do not have nltk, stopwords and wordnet already installed, follow below procedures:

```python
$ python
>>> import nltk
>>> nltk.download()
>>> nltk.download('stopwords')
```
