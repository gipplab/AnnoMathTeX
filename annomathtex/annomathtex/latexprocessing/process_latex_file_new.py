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
    #todo: adjust newline in all taggers and identifier retrievers

    #tagged_words = tagger.tag(line_chunk, endline)
    #cutoff = 7.0
    #for RAKE
    #tagged_words = identifier_retriever.extract_identifiers(line_chunk, endline, cutoff)
    #for Spacey
    #endline = True if '\n' in sentence else False
    tagged_words = identifier_retriever.extract_identifiers(sentence)

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
                word_window=None
            )
        )

    return processed_maths_env


def get_math_envs(file):
    tex_soup = TexSoup(file)
    equation = list(tex_soup.find_all('equation'))
    align = list(tex_soup.find_all('align'))
    dollar = list(tex_soup.find_all('$'))
    math_envs = equation + align + dollar
    return list(map(lambda m: str(m), math_envs))


def process_lines(request_file):
    """
    processes the file
    todo: check runtime with multiprocessing
    :param request_file: request.FILES['file'], the file that the user uploaded
    :return:
    """

    file = decode(request_file)
    math_envs = get_math_envs(file)


    for i, m in enumerate(math_envs):
        try:
            file = re.sub(m, '__MATH_ENV__', file, 1)
        except Exception as e:
            continue

    #print('\n' in file)
    split_at = r'(\n|\.|\?|!)'
    lines = [p for p in file.split('\n')]
    #sentences = [nltk.sent_tokenize(s) for s in paragraphs]
    #def add_to_list(p):
    #    return p if len(p) else '\n'
    #sentences = list(map(add_to_list(), paragraphs))


    #sentences = nltk.sent_tokenize(file)
    #l = filter(lambda x: '\n' in x, sentences)
    processed_lines = [extract_words(s, i) for i,s in enumerate(lines)]

    processed_sentences_including_maths = []
    for line in processed_lines:
        line_new = []
        if len(line) < 1:
            line_new.append(EmptyLine(uuid1()))
        for w in line:
            if re.search(r'__MATH_ENV__', w.content):
                line_new.append(extract_identifiers(w.content, 3))
            else:
                line_new.append(w)
        processed_sentences_including_maths.append(line_new)


    return processed_sentences_including_maths


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
    #for p in processed_lines:
    #    print(p)

    return LaTeXFile(processed_lines)



