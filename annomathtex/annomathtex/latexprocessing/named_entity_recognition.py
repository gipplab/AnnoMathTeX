import nltk
from .model.word import Word
from uuid import uuid1
import en_core_web_sm


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
    pass


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





