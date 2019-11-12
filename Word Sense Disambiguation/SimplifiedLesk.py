"""This module is an Implementation of Simplified Lesk algorithm for WSD."""
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class SimplifiedLesk:
    """Implement Lesk algorithm."""

    def __init__(self):
        self.stopwords = set(stopwords.words('english'))

    def disambiguate(self, word, sentence):
        """Return the best sense from wordnet for the word in given sentence.

        Args:
            word (string)       The word for which sense is to be found
            sentence (string)   The sentence containing the word

        """
        word_senses = wordnet.synsets(word)
        best_sense = word_senses[0]  # Assume that first sense is most freq.
        max_overlap = 0
        context = set(word_tokenize(sentence))
        for sense in word_senses:
            signature = self.tokenized_gloss(sense)
            overlap = self.compute_overlap(signature, context)
            if overlap > max_overlap:
                max_overlap = overlap
                best_sense = sense
        return best_sense

    def tokenized_gloss(self, sense):
        """Return set of token in gloss and examples"""
        tokens = set(word_tokenize(sense.definition()))
        for example in sense.examples():
            tokens.union(set(word_tokenize(example)))
        return tokens

    def compute_overlap(self, signature, context):
        """Returns the number of words in common between two sets.

        This overlap ignores function words or other words on a stop word list
        """
        gloss = signature.difference(self.stopwords)
        return len(gloss.intersection(context))


# Sample Driver code:

sentence = ("The bank can guarantee deposits will eventually cover future"
            " tuition costs because it invests in adjustable-rate mortgage"
            " securities.")
word = "bank"
lesk = SimplifiedLesk()
print ("Word :", word)
print ("Sentence :", sentence)
print ("Best sense: ", lesk.disambiguate(word, sentence))
