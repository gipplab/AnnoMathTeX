"""
This file contains several named entity taggers, that can be used to find NEs in the TeX file
"""



import nltk
from ...models.word import Word
from uuid import uuid1
import en_core_web_sm
from stanfordcorenlp import StanfordCoreNLP
from ..__latex_processing_config__ import __SCNLP_PATH__
import os

from abc import ABCMeta, abstractmethod


#these commands sometimes get recognized as NEs (or nouns,...)
#don't highlight these
#add others
latex_cmds_ignore = ['\\subsection',
                     '\\item',
                     '\\begin',
                     'enumerate',
                     '\\documentclass',
                     '\\usepackage',
                     '\\author',
                     '\\inputenc',
                     'babel',
                     'graphicx',
                     'amssymb',
                     'amsfonts',
                     'fontenc']


class Tagger(object, metaclass=ABCMeta):
    """
    Abstract base class for all NE taggers
    todo: implement
    """

    @abstractmethod
    def get_tags(self, line_chunk):
        raise NotImplementedError('must be implemented')

    def tag(self, line_chunk):
        word_tokens = self.get_tags(line_chunk)

        words = []

        try:

            for word, tag in word_tokens:
                is_ne = True if tag in self.tag_list and word not in latex_cmds_ignore else False
                #print(word, tag, is_ne)
                words.append(
                     Word(str(uuid1()),
                     type='Word',
                     highlight="green" if is_ne else "black",
                     content=word,
                     endline=True if str(word) == '\n' else False,
                     named_entity=is_ne,
                     wikidata_result=None)
                )


        except Exception as e:
            print(e)

        return words



def own_tagger(line_chunk):
    #use https://en.wikipedia.org/wiki/List_of_physical_quantities
    pass


class NLTK_NER(Tagger):
    """
    method tag called from abstract base class
    """

    def __init__(self):
        super().__init__()
        self.tag_list = ['NN', 'NNS', 'NNP', 'NNPS']

    def get_tags(self, line_chunk):
        word_tokens = nltk.word_tokenize(line_chunk)
        #print(word_tokens)
        word_tokens = nltk.pos_tag(word_tokens)
        return word_tokens



class StanfordCoreNLP_NER(Tagger):
    """
    has to be started in different terminal...
    """


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

    def kill_corenlp(self):
        self.nlp.close()
        return


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


    def get_tags(self, line_chunk):
        word_tokens = self.nlp.pos(line_chunk)
        self.kill_corenlp()
        return word_tokens



class Spacy_NER(Tagger):
    """
    Looks quite promising, as it has several 'types' that words are tagged with, one of which is 'QUANTITY'
    These can be accessed through word.ent_type

    https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

    Spacey has the feature of recognizing multiple words that belong together.
    Implemented this in identifier retrieval.
    """

    def __init__(self):
        super().__init__()
        self.nlp = en_core_web_sm.load()
        self.tag_list = ['NOUN', 'PROPN']


    def get_tags(self, line_chunk):
        word_tokens = [(word.text, word.pos_) for word in self.nlp(line_chunk)]
        #s = ["QUANTITY", "ORDINAL", "CARDINAL"]
        #test = [(word.text, word.ent_type_) for word in self.nlp(line_chunk) if word.ent_type_ in s]
        #if test: print(test)
        return word_tokens
