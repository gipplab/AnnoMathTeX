from os import path, getcwd
import nltk
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import os
from stanfordcorenlp import StanfordCoreNLP
import logging


basepath = path.dirname(__file__)
latexfolder = path.abspath(path.join(basepath, "../../.."))



def extract_words(line_chunk):
    """
    This method extracts the words that are contained in a line.
    If a named entity is contained, mark that.
    :param line_chunk: Part of line that is being processed (list of words).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Word() objects.
    """
    # todo: use NECKAR NER
    words = []
    word_tokens = nltk.word_tokenize(line_chunk)
    word_tokens = nltk.pos_tag(word_tokens)
    word_tokens = nltk.ne_chunk(word_tokens)


    tag_list = ['NN', 'NNS', 'NNP', 'NNPS']
    for _, word in enumerate(word_tokens):
        #if word[1] in tag_list:
        #    print(word)
        print(word, type(word))


    return word_tokens


@staticmethod
def start_corenlp():
    print("Starting CoreNLP Server")
    path_to_libs = os.path.join(os.path.dirname(__file__)) + "/resources/corenlp/stanford-corenlp-full-2018-10-05"
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
        #logging_level = logging.INFO)
        self.props = {
        'annotators':
        'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
        'pipelineLanguage': 'en',
        'outputFormat': 'json'
        }



def spacy_ner(line_chunk):
    nlp = en_core_web_sm.load()
    d = nlp(line_chunk)
    tag_list = ['NOUN', 'PROPN']
    for w in d:
        is_ne = True if w.pos_ in tag_list else False
        if is_ne:
            print(w)





ex1 = "You Google will have to download the pre-trained models(for the most part convolutional networks) separately. The limitations that you’ll face is that despite having a good amount of pre-trained models, they are mostly English or German. Mind you, they are extremely good and as far as performance is concerned, spaCy is absolutely astonishing. The other great thing about it is the brilliant documentation."

ex2 = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
#extract_words(ex)

ex3 = 'In physics, mass–energy equivalence states that anything having mass has an equivalent amount of energy and vice versa, with these fundamental quantities directly relating to one another by Albert Einstein\'s famous formula'
#extract_words(ex2)

#core_nlp(ex2)


spacy_ner(ex3)
