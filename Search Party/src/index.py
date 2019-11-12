"""Module represents wrapper for solr."""
import solr
from urllib2 import urlopen
import urllib


class SolrSearch:
    """A wrapper class for searchparty Solr index.

    Attributes:
        url   The Solr URL for the collection

    """
    fields = ["tokens","stems","phrases", "headword", "pos", "lemma",
              "hypernyms", "hyponyms", "substance_meronym", "member_meronym",
              "part_meronym", "substance_holonym", "member_holonym", "part_holonym", "synonyms"
              ]

    def __init__(self, url):
        """Initialize the wrapper with the search url.

        Args:
            url (string) The Solr URL for the searchparty collection
        """
        self.url = url
        self.conn = solr.SolrConnection(url)
        self.weightage = {}
        self.setWeigtage([10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

    def add_shallow(self, doc):
        """Index the shallow document in solr."""
        self.conn.add(id=doc["id"], tokens=doc["tokens"])
        self.conn.commit()


    def add(self, doc):
        """Index the document in solr."""
        self.conn.add(id=doc["id"], tokens=doc["tokens"], stems=doc["stems"],
                      phrases=doc["phrases"], headword=doc["headword"],
                      pos=doc["pos"], lemma=doc["lemma"], hypernyms=doc["hypernyms"],
                      hyponyms=doc["hyponyms"], substance_meronym=doc["substance_meronym"],
                      member_meronym=doc["member_meronym"],
                      part_meronym=doc["part_meronym"], substance_holonym=doc["substance_holonym"],
                      member_holonym=doc["member_holonym"], part_holonym=doc["part_holonym"],
                      sentence=doc["sentence"], synonyms=doc["synonyms"])
        self.conn.commit()

    def query(self, query):
        """Query input tokens."""
        query_url = self.url+"/select?fl=sentence,id&q="+ query
        query_url += "&" + self.queryFeatures()
        data = urllib.quote(query_url, safe="%/\()+,'\"&$:?=^!@$#*")
        connection = urlopen(data)
        response = eval(connection.read())
        # print "query formed: ", query_url
        # print response['response']['numFound'], "documents found."
        return response['response']['docs']

    def setWeigtage(self, weightage):
        """Return weightage for the query."""
        self.weightage = {}
        for idx, val in enumerate(weightage):
            if val != -1:
                self.weightage[self.fields[idx]] = val

    def queryFeatures(self):
        """Generate qf parameter for solr"""
        qf = "defType=edismax&qf="
        for key in self.weightage:
            qf = qf + key + "^" + str(self.weightage[key]) + "+"
        return qf


# fields = ["id", "tokens"]


# Driver Code:
# url = "http://localhost:8983/solr/searchparty"
# s = SolrSearch(url)
# wts = [ 10, 0, 0, 0, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1 ]
# s.setWeigtage(wts)
# s.query(["MTBE","plant","in","canada"])
