from nltk.corpus import stopwords
import codecs
from nltk.tokenize import word_tokenize
class classifier:
    
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))
        
                
    def remove_stopword(self, words):
        filtered_words = []
        for w in words:
            if w not in self.stopwords:
                filtered_words.append(w)
        return filtered_words
    
    def read_file(self, file_path):
        with codecs.open(file_path, "r",encoding='utf-8', errors='replace') as fdata:
            return word_tokenize(fdata.read())
        