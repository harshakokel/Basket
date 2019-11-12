"""Module represents querying to Solr."""
import index
import deeperpipeline as dp
from nltk.tokenize import word_tokenize
import xlsxwriter
import datetime


class Search:
        """Implementing Search.

        Attributes:
            url     The Solr URL for the collection

        """

        def __init__(self, url):
            self.solr = index.SolrSearch(url)
            self.deepernlp = dp.DeeperPipeline(url, True)

        def shallow_search(self, sentences):
            """Return top 10 relevant search result for given string."""
            workbook = xlsxwriter.Workbook(str(datetime.datetime.now())+"_shallownlp"+ '.xlsx')
            worksheet = self.create_excel(workbook)
            i = 0
            docs = []
            for sentence in sentences:
                docs = self.solr.query("tokens:"+"+".join(word_tokenize(sentence)))
                self.write_to_excel(sentence, docs, i, worksheet)
                i += 1
            workbook.close()
            return docs


        def deeper_search(self, sentences):
            """Return top 10 relevant search result for given string."""
            #fields = ["tokens","stems","phrases", "headword", "pos", "lemma",
              # "hypernyms", "hyponyms", "substance_meronym", "member_meronym",
              # "part_meronym", "substance_holonym", "member_holonym", "part_holonym", "synonyms"
              # ]
            wts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.solr.setWeigtage(wts)
            workbook = xlsxwriter.Workbook(str(datetime.datetime.now())+"_deepernlp"+ '.xlsx')
            worksheet = self.create_excel(workbook)
            i = 0
            docs = []
            for sentence in sentences:
                tokens = word_tokenize(sentence)
                query = 'tokens:'+ "+".join(tokens)
                query += ',stems:'+ "+".join(self.deepernlp.stem(tokens))
                dependency_parse, headword = self.deepernlp.dep_parse_and_headword(tokens)
                query += ',headword:'+ headword
                POS = self.deepernlp.POS(tokens)
                query += ',lemma:' + "+".join(self.deepernlp.lemma(POS))+',pos:'
                for p in POS:
                    query += str(p)
                hypernyms = filter(None, self.deepernlp.hypernym(tokens))
                if len(hypernyms) > 0:
                    query += ',hypernyms:' + "+".join(hypernyms)
                hyponyms = filter(None, self.deepernlp.hyponym(tokens))
                if len(hyponyms) > 0:
                    query += ',hyponyms:' + "+".join(hyponyms)
                s_meronyms = filter(None, self.deepernlp.substance_meronym(tokens))
                if len(s_meronyms) > 0:
                    query += ',substance_meronym:' + "+".join(s_meronyms)
                m_meronyms = filter(None, self.deepernlp.member_meronym(tokens))
                if len(m_meronyms) > 0:
                    query += ',member_meronym:' + "+".join(m_meronyms)
                p_meronyms = filter(None, self.deepernlp.part_meronym(tokens))
                if len(p_meronyms) > 0:
                    query += ',part_meronym:' + "+".join(p_meronyms)
                s_holonyms = filter(None, self.deepernlp.substance_holonym(tokens))
                if len(s_holonyms) > 0:
                    query += ',substance_holonym:' + "+".join(s_holonyms)
                m_holonyms = filter(None, self.deepernlp.member_holonym(tokens))
                if len(m_holonyms) > 0:
                    query += ',member_holonym:' + "+".join(filter(None,m_holonyms))
                p_holonyms = filter(None, self.deepernlp.part_holonym(tokens))
                if len(p_holonyms) > 0:
                    query += ',part_holonym:' + "+".join(p_holonyms)
                # print query
                docs = self.solr.query(query)
                self.write_to_excel(sentence, docs, i, worksheet)
                i += 1
            workbook.close()
            return docs

        def custom_search(self, sentences):
            """Return top 10 relevant search result for given string."""
            #fields = ["tokens","stems","phrases", "headword", "pos", "lemma",
              # "hypernyms", "hyponyms", "substance_meronym", "member_meronym",
              # "part_meronym", "substance_holonym", "member_holonym", "part_holonym", "synonyms"
              # ]
            wts = [2, -1, -1, -1, -1, 0, 0, 0, -1,-1,-1,-1,-1,-1,1]
            self.solr.setWeigtage(wts)
            workbook = xlsxwriter.Workbook(str(datetime.datetime.now())+"_custom"+ '.xlsx')
            worksheet = self.create_excel(workbook)
            i = 0
            docs = []
            for sentence in sentences:
                tokens = word_tokenize(sentence)
                query = 'tokens:'+ "+".join(tokens)
                query = 'synonyms:'+ "+".join(self.deepernlp.stem(tokens))
                query += ',stems:'+ "+".join(self.deepernlp.stem(tokens))
                POS = self.deepernlp.POS(tokens)
                query += ',lemma:' + "+".join(self.deepernlp.lemma(POS))
                hypernyms = filter(None, self.deepernlp.hypernym(tokens))
                hyponyms = filter(None, self.deepernlp.hyponym(tokens))
                query += ',hypernyms:' + "+".join(hypernyms)
                query += ',hyponyms:' + "+".join(hyponyms)
                docs = self.solr.query(query)
                self.write_to_excel(sentence, docs, i, worksheet)
                i += 1
            workbook.close()
            return docs

        def create_excel(self, workbook):
            """Create an new Excel file and add a worksheet."""
            worksheet = workbook.add_worksheet()
            text = workbook.add_format()
            text.set_text_wrap()
            worksheet.set_column(1, 1, 150, text)
            highlight = workbook.add_format()
            highlight.set_bold()
            worksheet.set_column(0, 0, 20, highlight)
            worksheet.write(0, 1, "Sentence", )
            worksheet.write(0, 2, "ID")
            worksheet.write(0, 3, "Relevance")
            return worksheet

        def write_to_excel(self, query, results, i, worksheet):
            worksheet.write((1 + (11*i)), 0, "Query")
            worksheet.merge_range((2 + (11*i)), 0, (11 + (11*i)), 0, "Results")
            worksheet.write((1 + (11*i)), 1, query)
            row = (2 + (11*i))
            for result in results:
                # print result["sentence"][0]
                worksheet.write(row, 1, result["sentence"][0])
                worksheet.write(row, 2, result["id"])
                row += 1

        def search(self, sentence, id=0):
            sentences = [sentence]
            results = []
            if id == 1:
                print 'Running deeper NLP search ...'
                results = self.deeper_search(sentences)
            elif id == 2:
                print 'Running custom NLP search ...'
                results = self.custom_search(sentences)
            else:
                print 'Running shallow NLP search ...'
                results = self.shallow_search(sentences)
            print "Top 10 results:"
            for result in results:
                print result["id"], ": ", result["sentence"][0]



# Driver Code
url = "http://129.110.92.21:8983/solr/searchparty"
s = Search(url)
# s.search("largest copper manufacturer", 2)
query = []

# query.append("Sugar factory shut because of importing sugar") #2
# query.append("largest copper manufacturer")  #3
# query.append("paris agreement on foreign exchange rates") #4
# query.append("Bowaters profit exceeds market expectation") #5
# query.append("People having good time in US") #1
# query.append("liquidity in market guiding interest rates") #6
# query.append("attacks on ports of Newcastle")  #7
# query.append("Why did Korea switch back to U S corn supply?") #8
# query.append("India's target of foodgrain production by 1990") #9
# query.append("oil companies to decide oil prices in Singapore")

query.append("effects of sudden fall in temperature")

s.shallow_search(query)
s.deeper_search(query)
s.custom_search(query)
