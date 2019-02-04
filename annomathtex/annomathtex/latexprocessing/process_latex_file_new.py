import re
import nltk
from uuid import uuid1
from .model.word import Word
from .model.identifier import Identifier
from .model.empty_line import EmptyLine
from .model.latexfile import LaTeXFile
from .named_entity_handling import NESparql
#from .math_environment_handling import MathSparql
from .named_entity_recognition import NLTK_NER, StanfordCoreNLP_NER, Spacy_NER
from .identifier_retrieval import RakeIdentifier, SpaceyIdentifier
import json
import time
from .latexformlaidentifiers import FormulaSplitter
from collections import OrderedDict
from TexSoup import TexSoup



def decode(request_file):
    """
    TeX files are in bytes and have to be converted to string in utf-8
    :return: list of lines (string)
    """
    bytes = request_file.read()
    string = bytes.decode('utf-8')
    #string_split = string.splitlines(1)
    return string


def extract_words(sentence, line_num):
    """
    This method extracts the words that are contained in a line.
    If a named entity is contained, mark that.
    todo: some kind of metric as to how far in the document the nearest math environment is
    :param line_chunk: Part of line that is being processed (list of words).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Word() objects.
    """
    #select between NE tagging and keyword extraction


    #tagged_words = tagger.tag(line_chunk, endline)
    #cutoff = 7.0
    #for RAKE
    #tagged_words = identifier_retriever.extract_identifiers(line_chunk, endline, cutoff)
    #for Spacey
    endline = True if '\n' in sentence else False
    tagged_words = identifier_retriever.extract_identifiers(sentence, endline)

    #add named entities from this line to __line_dict
    #__line_dict[line_num] = [word for word in tagged_words if word.named_entity]
    return tagged_words


def entire_formula(line_chunck, endline):
    pass


def extract_identifiers(math_env, line_num):
    """
    This method should only look at extracting identifiers from the line_chunk.
    Handle the entire formula in another method.
    This method extracts the identifiers that are contained in a line.
    :param line_chunk: Part of line that is being processed (list of words or maths env).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Identifier() objects.
    """

    identifiers = FormulaSplitter(math_env).get_identifiers()


    word_window = None

    split_regex = "|".join(str(i) for i in identifiers)
    split_regex = r"({})".format(split_regex)

    split_math_env = re.split(split_regex, math_env)


    processed_maths_env = []
    for symbol in split_math_env:
        if symbol in identifiers:
            wikidata_result = mathsparql.broad_search(symbol)
        else:
            wikidata_result = None

        endline = True if symbol == '\n' else False

        processed_maths_env.append(
            Identifier(
                str(uuid1()),
                type='Identifier',
                highlight='pink',
                content=symbol,
                endline=endline,
                wikidata_result=json.dumps({'w': wikidata_result}),
                word_window=word_window
            )
        )



    #add the dollar signs back again
    """dollar = Identifier(
                str(uuid1()),
                type='Identifier',
                highlight='yellow',
                content='$',
                endline=False,
                wikidata_result = None,
                word_window=None
            )

    processed_maths_env = [dollar] + processed_maths_env + [dollar]

    if endline:
        processed_maths_env[-1].endline = True"""


    return processed_maths_env


def get_math_envs(file):
    tex_soup = TexSoup(file)
    math_envs = list((tex_soup.find_all('equation'), tex_soup.find_all('align'), list(tex_soup.find_all('$'))))
    return math_envs


def process_lines(request_file):
    """
    processes the file
    todo: check runtime with multiprocessing
    :param request_file: request.FILES['file'], the file that the user uploaded
    :return:
    """

    file = decode(request_file)
    math_envs = get_math_envs(file)
    """for m in math_envs:
        try:
            file = file.replace(m, '')
        except:
            continue"""

    #split file on math_envs
    #split_string = '|'.join(m for m in math_envs)
    #split_string = r'({})'.format(split_string)
    #split_file = re.split(split_string, file)


    for i, m in enumerate(math_envs):
        file = re.sub(m, '__MATH_ENV__{}'.format(i), 1)

    sentences = nltk.sent_tokenize(file)
    processed_sentences = [extract_words(s, i) for i,s in enumerate(sentences)]

    all_sentences = []
    for ps in processed_sentences:

        ps_new = []
        for w in ps:
            if re.search(r'__MATH_ENV__[0-9]+', w.content):
                ps_new.append(extract_identifiers(w.content))
            else:ps_new.append(w)

        all_sentences.append(ps_new)


    return all_sentences











def get_processed_file(request_file):
    """

    :param request_file:
    :return:
    """
    #possible taggers
    #tagger_names = ['NLTK_NER_1', 'NLTK_NER_2', 'StanfordCoreNLP_NER', 'Spacy_NER']


    global tagger, identifier_retriever, nesparql, mathsparql
    nesparql = NESparql()
    # mathsparql = MathSparql()
    tagger = NLTK_NER()
    #identifier_retriever = RakeIdentifier()
    identifier_retriever = SpaceyIdentifier()
    #tagger = Spacy_NER()
    #tagger = StanfordCoreNLP_NER()

    processed_lines = process_lines(request_file)

    return LaTeXFile(processed_lines)



