# Search Party

This project is implemented as part of CS 6320 - Natural Language Processing at University of Texas Dallas by **Harsha Kokel** and **Shakti Suman**.

It is an implemention of a semantic search application that will produce improved results using NLP features and techniques. Project implements a keyword-based strategy and an improved strategy using NLP feature and techniques.

The implementation is divided in 4 parts which were provided as 4 Tasks for the project. The 'Instruction' section in each part is a copy of the Instruction provided where as 'Implementation' section provides the details about our project.

#### 1. Corpus:

###### Instruction  
Create a corpus of News articles. Your corpus should contain at least:  
o 1,000 articles  
o 100,000 words  

Note: you are free to download freely and publicly available News articles corpora from
public websites such as: http://www.nltk.org/nltk_data/

###### Implementation  

We would be working with **The Reuters-21578 benchmark corpus, ApteMod version** corpus of NLTK.

Details of the corpus are mentioned below.

*id*: reuters  
*size*: 6378691  
*license*: The copyright for the text of newswire articles and Reuters annotations in the Reuters-21578 collection resides with Reuters Ltd. Reuters Ltd. and Carnegie Group, Inc. have agreed to allow the free distribution of this data **for research purposes only**. If you publish results based on this data set, please acknowledge its use, refer to the data set by the name 'Reuters-21578, Distribution 1.0', and inform your readers of the current location of the data set.  
*url*: http://www.nltk.org/nltk_data/


#### 2. Shallow NLP Pipeline:

###### Instruction  
Implement a shallow NLP pipeline to perform the following:  
- Keyword search index creation  
  - [x]  Segment the News articles into sentences  
  - [x]  Tokenize the sentences into words  
  - [x]  Index the word vector per sentence into search index such as Lucene or SOLR  
- Natural language query parsing and search  
  - [x]  Segment an user’s input natural language query into sentences  
  - [x]  Tokenize the sentences into words  
  - [x]  Run a search/match with the search query word vector against the sentence word vector (present in the Lucene/SOLR search index) created from the corpus  
- Evaluate the results of at least 10 search queries for the top-10 returned sentence matches

###### Implementation

We used solrpy, a python client for the Solr search service to index the word vector for each sentences.

**index.py** file includes the implementation of wrapper class which uses solrpy to index sentences in solr.

**shallowpipeline.py** file includes the implementation of shallow nlp pipeline as per task 2.

Here is a sequence of commands to index the whole Reuters Corpus

```python
import shallowpipeline as sp
url = "http://localhost:8983/solr/searchparty"
shallownlp = sp.ShallowPipeline(url, False)
shallownlp.index_sentences()
```

To index individual sentence you can follow this code

```python
import shallowpipeline as sp
url = "http://localhost:8983/solr/searchparty"
shallownlp = sp.ShallowPipeline(url, False)
shallownlp.index_sentence('This is a demo sentence', 'demo_1')
```

To search by matching the tokens of the query, you can use search function as shown below.

```python
import search
url = "http://localhost:8983/solr/searchparty"
s = search.Search(url)
>>> s.search("People having good time in US", 0)
```

### 3. Deeper NLP pipeline:  

###### Instruction  
Implement a deeper NLP pipeline to perform the following: o Semantic search index creation
- Segment the News articles into sentences
  - [x] Tokenize the sentences into words
  - [x] Lemmatize the words to extract lemmas as features
  - [x] Stem the words to extract stemmed words as features
  - [x] Part-of-speech (POS) tag the words to extract POS tag features
  - [x] Syntactically parse the sentence and extract phrases, head words, OR dependency parse relations as features
  - [x] Using WordNet, extract hypernymns, hyponyms, meronyms, AND holonyms as features
  - [x] Index the various NLP features as separate search fields in a search index such as Lucene or SOLR
- Natural language query parsing and search
  - [x] Run the above described deeper NLP on an user’s input natural language and extract search query features
  - [x] Run a search/match against the separate or combination of search index fields created from the corpus
- Evaluate the results of at least 10 search queries for the top-10 returned sentence matches


###### Implementation  

**deeperpipeline.py** file includes the implementation of shallow nlp pipeline as per task 2.

Here is a sequence of commands to index the whole Reuters Corpus

```python
>>> import deeperpipeline as dp
>>> url = "http://localhost:8983/solr/searchparty"
>>> deepernlp = dp.DeeperPipeline(url, False)
>>> deepernlp.index_sentences()
```

To index individual sentence you can follow this code

```python
>>> import deeperpipeline as dp
>>> url = "http://localhost:8983/solr/searchparty"
>>> deepernlp = dp.DeeperPipeline(url, False)
>>> deepernlp.index_sentence('largest copper manufacturer', 'demo_2')
```

To search by matching full feature vector of the query, you can use search function as shown below.

```python
>>> import search
>>> url = "http://localhost:8983/solr/searchparty"
>>> s = search.Search(url)
>>> s.search("largest copper manufacturer", 1)
```

#### 4. Improve result:

###### Instruction  
Improve the shallow NLP pipeline results using a combination of deeper NLP pipeline features

###### Implementation  

We have improved the shallow NLP pipeline by including the lemmas, stems, hypernyms, holonyms and synonyms.

To search by custom feature vector, you can use search function as shown below.

```python
>>> import search
>>> url = "http://localhost:8983/solr/searchparty"
>>> s = search.Search(url)
>>> s.search("largest copper manufacturer", 1)
```


---

#### Prerequisite

To make this project work, we will need following setups.

1.  Install Python 2.7
2.  Download reuters corpus.
pip install nltk
    ```python  
    >>> import nltk
    >>> nltk.download('reuters')
    ```

3. Install solr
4. Use the managed-schema in the resources folder to create a core in Solr.
5. Install solrpy

    ```bash
    $ sudo pip install solrpy
    ```
6. Download stanford parser
7. Download stanford NER tagger
8. Download Perceptron tagger
nltk.download('averaged_perceptron_tagger')
9. Import XlsxWriter
   ```bash
   $ sudo pip install XlsxWriter
   ```


---
## References

1. https://blog.manash.me/configuring-stanford-parser-and-stanford-ner-tagger-with-nltk-in-python-on-windows-f685483c374a
2. NLTK: http://www.nltk.org/
3. Stanford NLP: http://nlp.stanford.edu/software/corenlp.shtml
4. Apache OpenNLP: http://opennlp.apache.org/
