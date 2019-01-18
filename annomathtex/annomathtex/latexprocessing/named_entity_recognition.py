import nltk
from .model.word import Word
from uuid import uuid1
import en_core_web_sm
from stanfordcorenlp import StanfordCoreNLP
from .__latex_processing_config__ import __SCNLP_PATH__
from abc import ABCMeta, abstractmethod
import os


def own_tagger(line_chunk):
    #use https://en.wikipedia.org/wiki/List_of_physical_quantities
    pass



class NLTK_NER_1:
    def tag(self, line_chunk, endline):
        word_tokens = nltk.word_tokenize(line_chunk)
        word_tokens = nltk.pos_tag(word_tokens)

        words = []

        tag_list = ['NN', 'NNS', 'NNP', 'NNPS']
        for _, word in enumerate(word_tokens):
            is_ne = True if word[1] in tag_list else False
            words.append(
                Word(str(uuid1()), type='Word', highlight="black", content=word, endline=False, named_entity=is_ne)
            )

        if endline:
            words[-1].endline = True

        return words



class NLTK_NER_2:
    def tag(self, line_chunk, endline):
        #Not sure if necessary
        words = []
        word_tokens = nltk.word_tokenize(line_chunk)
        word_tokens = nltk.pos_tag(word_tokens)
        word_tokens = nltk.ne_chunk(word_tokens)

        tag_list = ['NN', 'NNS', 'NNP', 'NNPS']
        for _, word in enumerate(word_tokens):
            # if word[1] in tag_list:
            #    print(word)
            print(word, type(word))

        if endline:
            words[-1].endline = True



class StanfordCoreNLPNER:

    def __init__(self):
        self.start_corenlp()
        self.nlp = self.SCNLP()

    def start_corenlp(self):
        """
        Only has to be started once
        When to kill?
        :return:
        """
        print("Starting CoreNLP Server")
        # path_to_libs = os.path.join(os.path.dirname(__file__)) + "/resources/corenlp/stanford-corenlp-full-2018-10-05"
        path_to_libs = __SCNLP_PATH__
        command = "cd " + path_to_libs + "; java -mx4g -cp '*' edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators 'tokenize,ssplit,pos,lemma,parse,sentiment' -port 9000 -timeout 30000 -props edu/stanford/nlp/coref/properties/neural-english.properties"
        os.system(command)


    class SCNLP:
        def __init__(self, host='http://localhost', port=9000):
            """
            Initializes connection to the localhost StanfordCoreNLP server
            :param host: hostname of the local server
            :param port: of the server
            """
            self.nlp = StanfordCoreNLP(host, port=port,
                                       timeout=30000)
            # logging_level = logging.INFO)
            self.props = {
                'annotators':
                    'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
                'pipelineLanguage': 'en',
                'outputFormat': 'json'
            }

        def pos(self, sentence):
            return self.nlp.pos_tag(sentence)

        def ner(self, sentence):
            return self.nlp.ner(sentence)

    def tag(self, line_chunk, endline):

        words = []
        word_tokens = self.nlp.pos(line_chunk)
        tag_list = ['NN', 'NNS', 'NNP', 'NNPS']
        for _, word in enumerate(word_tokens):
            is_ne = True if word[1] in tag_list else False
            words.append(
                Word(str(uuid1()), type='Word', highlight="black", content=word, endline=False, named_entity=is_ne)
            )

        if endline:
            words[-1].endline = True

        return words


class Spacy_NER:

    def __init__(self):
        self.nlp = en_core_web_sm.load()

    def tag(self, line_chunk, endline):
        words = []

        word_tokens = self.nlp(line_chunk)
        tag_list = ['NOUN', 'PROPN']
        for word in word_tokens:
            is_ne = True if word.pos_ in tag_list else False
            words.append(
                Word(str(uuid1()), type='Word', highlight="black", content=word, endline=False, named_entity=is_ne)
            )

        if endline:
            words[-1].endline = True

        return words






