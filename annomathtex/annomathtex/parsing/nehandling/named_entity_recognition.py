"""
This file contains several named entity taggers, that can be used to find NEs in the document.
"""

import nltk
from ...models.word import Word
from uuid import uuid1
from nltk.corpus import stopwords

from abc import ABCMeta, abstractmethod


# These commands sometimes get recognized as NEs (or nouns,...)
# Exclude these from highlighting
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
                     'fontenc',
                     ]

stopWords = list(set(stopwords.words('english')))
punctuation_nums = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+',
               ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
               '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

wikitext_cmds = ['sub', 'center', 'nbsp', 'ref', 'IEEE', 'ndash', 'Cite']
ignore = latex_cmds_ignore + stopWords + punctuation_nums + wikitext_cmds


class Tagger(object, metaclass=ABCMeta):
    """
    Abstract base class for all NE taggers
    """

    @abstractmethod
    def get_tags(self, line):
        """
        Tag the words that are pased in the line with the corresponding part of speech tag.
        :param line: A line of tokens (usually a sentence).
        :return: A list of tagged words.
        """
        raise NotImplementedError('must be implemented')

    def check_is_ne(self, word, tag):
        """
        Check whether the current word is a named entity. Tex and wikitext documents contain a lot of extra information
        (e.g. 'volume=28|issue=1|pages=100') which get tagged by the NE tagger as named entities. This method adds a
        few custom checks to make sure that they will not be highlighted as named entities.
        :param word:
        :param tag:
        :return:
        """
        max_word_length = 12
        min_word_length = 3

        is_ne = True if tag in self.tag_list and \
                word not in ignore and \
                len(word) <= max_word_length and \
                len(word) >= min_word_length and \
                not list(filter(lambda c: c in punctuation_nums, word)) else False

        return is_ne


    def tag(self, line):
        """
        This method loops through the words in the line and creates Word objects from them, adding the flag for named
        entities if applicable.
        :param line: A line of tokens (usually a sentence).
        :return: A list of the processed line (or sentence).
        """
        word_tokens = self.get_tags(line)
        colour = '#973c97'
        words = []

        try:

            for word, tag in word_tokens:
                is_ne = self.check_is_ne(word, tag)
                words.append(
                     Word(str(uuid1()),
                     type='Word',
                     highlight=colour if is_ne else "black",
                     content=word,
                     endline=True if str(word) == '\n' else False,
                     named_entity=is_ne
                     )
                )


        except Exception as e:
            print(e)

        return words


class NLTK_NER(Tagger):
    """
    The basic NLTK tagger
    """

    def __init__(self):
        super().__init__()
        #Words with these tags are considered as named entities
        self.tag_list = ['NN', 'NNS', 'NNP', 'NNPS']

    def get_tags(self, line):
        word_tokens = nltk.word_tokenize(line)
        word_tokens = nltk.pos_tag(word_tokens)
        return word_tokens







###################################################################################
###################################################################################
###################################################################################
#################################### NOT USED #####################################
###################################################################################
###################################################################################
###################################################################################

"""
#import en_core_web_sm
#from stanfordcorenlp import StanfordCoreNLP
#from ..__latex_processing_config__ import __SCNLP_PATH__

class StanfordCoreNLP_NER(Tagger):
    #has to be started in different terminal...
    


    def __init__(self):
        self.start_corenlp()
        self.nlp = self.SCNLP()

    def start_corenlp(self):
        #Only has to be started once
        #When to kill?
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
            #Initializes connection to the localhost StanfordCoreNLP server
            #:param host: hostname of the local server
            #:param port: of the server
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
    
    #Looks quite promising, as it has several 'types' that words are tagged with, one of which is 'QUANTITY'
    #These can be accessed through word.ent_type

    #https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

    #Spacey has the feature of recognizing multiple words that belong together.
    #Implemented this in identifier retrieval.
    

    def __init__(self):
        super().__init__()
        #self.nlp = en_core_web_sm.load()
        self.nlp = None
        self.tag_list = ['NOUN', 'PROPN']


    def get_tags(self, line_chunk):
        word_tokens = [(word.text, word.pos_) for word in self.nlp(line_chunk)]
        #s = ["QUANTITY", "ORDINAL", "CARDINAL"]
        #test = [(word.text, word.ent_type_) for word in self.nlp(line_chunk) if word.ent_type_ in s]
        #if test: print(test)
        return word_tokens"""
