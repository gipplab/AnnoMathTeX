from os import path, getcwd
import nltk
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import os
#from stanfordcorenlp import StanfordCoreNLP


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


def core_nlp(line_chunk):
    #os.system('cd ~ & ls')
    #nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)
    #print(nlp.word_tokenize(line_chunk))
    #print(nlp.ner(line_chunk))
    pass


def spacy_ner(line_chunk):
    nlp = en_core_web_sm.load()
    d = nlp(line_chunk)
    for w in d:
        #print(w, w.ent_type_, w.pos_)
        print(w, w.pos_)


ex1 = "You Google will have to download the pre-trained models(for the most part convolutional networks) separately. The limitations that you’ll face is that despite having a good amount of pre-trained models, they are mostly English or German. Mind you, they are extremely good and as far as performance is concerned, spaCy is absolutely astonishing. The other great thing about it is the brilliant documentation."

ex2 = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
#extract_words(ex)

ex3 = 'In physics, mass–energy equivalence states that anything having mass has an equivalent amount of energy and vice versa, with these fundamental quantities directly relating to one another by Albert Einstein\'s famous formula'
#extract_words(ex2)

#core_nlp(ex2)


spacy_ner(ex2)
