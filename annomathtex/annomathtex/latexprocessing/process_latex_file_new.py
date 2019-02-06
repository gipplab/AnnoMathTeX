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

__line_dict = {}


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
    #tagged_words = tagger.tag(line_chunk)
    #for RAKE & Spacey
    tagged_words = identifier_retriever.extract_identifiers(sentence)


    #add named entities from this line to __line_dict
    __line_dict[line_num] = [word for word in tagged_words if word.named_entity]
    return tagged_words


def get_word_window(line_num):
    #word_window = [__line_dict[n] for ]
    word_window = []
    for n in [line_num, line_num-1, line_num+1, line_num-2, line_num+2]:
        if n in __line_dict:
            word_window += __line_dict[n]

    #print(word_window)

    return word_window


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

    #todo: for all math environemnt markers
    math_env = math_env.replace('$', '')

    identifiers = FormulaSplitter(math_env).get_identifiers()
    #print(identifiers)

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
                word_window=get_word_window(line_num)
            )
        )

    # add the dollar signs back again
    dollar = Identifier(
        str(uuid1()),
        type='Identifier',
        highlight='yellow',
        content='$',
        endline=False,
        wikidata_result=None,
        word_window=None
        )

    processed_maths_env = [dollar] + processed_maths_env + [dollar]

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
            file = file.replace(m, '__MATH_ENV__', 1)
        except Exception as e:
            print('Line 137: ', e)
            continue


    lines = [p for p in file.split('\n')]
    #print(lines)

    processed_lines = [extract_words(s, i) for i,s in enumerate(lines)]

    processed_sentences_including_maths = []
    for line_num, line in enumerate(processed_lines):
        line_new = []
        if len(line) < 1:
            line_new.append(EmptyLine(uuid1()))
        for w in line:
            #print(w.content)
            if re.search(r'__MATH_ENV__', w.content):
                #print(w.content)
                #print('extracting identifers', w.content)
                math_env = math_envs[0]
                math_envs.pop(0)
                #line_new.append(extract_identifiers(math_env, line_num))
                foo = extract_identifiers(math_env, line_num)
                #print(foo)
                line_new += foo
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
    identifier_retriever = RakeIdentifier()
    #identifier_retriever = SpaceyIdentifier()
    #tagger = Spacy_NER()
    #tagger = StanfordCoreNLP_NER()

    processed_lines = process_lines(request_file)
    return LaTeXFile(processed_lines)



