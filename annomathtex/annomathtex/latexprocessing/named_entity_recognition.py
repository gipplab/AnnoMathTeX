import nltk
from .model.word import Word
from uuid import uuid1
import en_core_web_sm
from stanfordcorenlp import StanfordCoreNLP
from .__latex_processing_config__ import __SCNLP_PATH__
import os


def own_tagger(line_chunk):
    #use https://en.wikipedia.org/wiki/List_of_physical_quantities
    pass


def nlt_ner_1(line_chunk):
    word_tokens = nltk.word_tokenize(line_chunk)
    word_tokens = nltk.pos_tag(word_tokens)

    words = []

    tag_list = ['NN', 'NNS', 'NNP', 'NNPS']
    for _, word in enumerate(word_tokens):
        is_ne = True if word[1] in tag_list else False
        words.append(
            Word(str(uuid1()), type='Word', highlight="black", content=word, endline=False, named_entity=is_ne)
        )

    return words

def nlt_ner_2(line_chunk):
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


def stanford_core_nlp_ner(line_chunk):

    def start_corenlp():
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

    start_corenlp()
    nlp = SCNLP()

    words = []
    word_tokens = nlp.pos(line_chunk)
    tag_list = ['NN', 'NNS', 'NNP', 'NNPS']
    for _, word in enumerate(word_tokens):
        is_ne = True if word[1] in tag_list else False
        words.append(
            Word(str(uuid1()), type='Word', highlight="black", content=word, endline=False, named_entity=is_ne)
        )

    return words




def spacy_ner(line_chunk):
    words = []
    nlp = en_core_web_sm.load()
    word_tokens = nlp(line_chunk)
    tag_list = ['NOUN', 'PROPN']
    for word in word_tokens:
        is_ne = True if word.pos_ in tag_list else False
        words.append(
            Word(str(uuid1()), type='Word', highlight="black", content=word, endline=False, named_entity=is_ne)
        )

    return words


def handle(line_chunk, endline, ner='nltk_ner_1'):

    if ner == 'nltk_ner_1':
        words = nlt_ner_1(line_chunk)
    elif ner == 'nltk_ner_2':
        words = nlt_ner_2(line_chunk)
    elif ner == 'stanford_core_nlp_ner':
        words = stanford_core_nlp_ner(line_chunk)
    elif ner == 'spacy_ner':
        words = spacy_ner(line_chunk)

    if endline:
        words[-1].endline = True

    return words





