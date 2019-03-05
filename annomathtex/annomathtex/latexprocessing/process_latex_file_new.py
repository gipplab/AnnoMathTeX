import re
import nltk
from uuid import uuid1
from .model.word import Word
from .model.identifier import Identifier
from .model.formula import Formula
from .model.empty_line import EmptyLine
from .model.latexfile import LaTeXFile
from .named_entity_handling import NESparql
from .math_environment_handling import MathSparql as mathsparql
from .named_entity_recognition import NLTK_NER, StanfordCoreNLP_NER, Spacy_NER
from .identifier_retrieval import RakeIdentifier
from .evaluation_list_handling import ArXivEvaluationListHandler, WikipediaEvaluationListHandler
import json
import time
from .latexformlaidentifiers import FormulaSplitter
from collections import OrderedDict
from TexSoup import TexSoup

__line_dict = {}


def decode(request_file):
    """
    TeX evaluation_files are in bytes and have to be converted to string in utf-8
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
    tagged_words = tagger.tag(sentence)
    #for RAKE & Spacey
    #tagged_words = identifier_retriever.extract_identifiers(sentence)


    #add named entities from this line to __line_dict

    #for w in tagged_words:
    #    if w.named_entity:
    #        print(w)

    __line_dict[line_num] = [word for word in tagged_words if word.named_entity]
    return tagged_words


def get_word_window(line_num):
    #todo: make class, to be consistent
    #word_window = [__line_dict[n] for ]
    word_window = []
    for n in [line_num, line_num-1, line_num+1, line_num-2, line_num+2]:
        if n in __line_dict:
            for word in __line_dict[n]:
                #print(word.content)
                word_window.append({
                    'content': word.content,
                    'unique_id': word.unique_id
                })


    if not word_window:
        word_window = [{}]


    return word_window


def entire_formula(math_env):

    #for some reason django
    #math_env = math_env.replace('=', '__EQUALS__')

    formula1 = Formula(
        str(uuid1()),
        type='Formula',
        highlight='yellow',
        content='$',
        endline=False,
        wikidata_result=None,
        word_window=None,
        arXiv_evaluation_items=None,
        wikipedia_evaluation_items=None,
        math_env=math_env
    )

    formula2 = Formula(
        str(uuid1()),
        type='Formula',
        highlight='yellow',
        content='$',
        endline=False,
        wikidata_result=None,
        word_window=None,
        arXiv_evaluation_items=None,
        wikipedia_evaluation_items=None,
        math_env=math_env
    )


    return formula1, formula2








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

    print('MATH_ENV:', math_env)

    identifiers = FormulaSplitter(math_env).get_identifiers()
    print('Identifiers:', identifiers, type(identifiers))
    for i in identifiers:
        print(i, type(i))

    split_regex = "|".join(str(i) for i in identifiers)
    split_regex = r"({})".format(split_regex)

    #todo: not working right
    split_math_env = re.split(split_regex, math_env)
    print('Spit math env:', split_math_env)

    processed_maths_env = []
    for symbol in split_math_env:
        print('Symbol:', symbol)
        if symbol in identifiers:
            #wikidata_result = mathsparql.broad_search(symbol)
            wikidata_result=None
            arXiv_evaluation_items = arXiv_evaluation_list_handler.check_identifiers(symbol)
            wikipedia_evaluation_items = wikipedia_evaluation_list_handler.check_identifiers(symbol)
        else:
            print('symbol {} not in identifiers'.format(symbol))
            wikidata_result = None
            arXiv_evaluation_items =None
            wikipedia_evaluation_items =None

        endline = True if symbol == '\n' else False

        processed_maths_env.append(
            Identifier(
                str(uuid1()),
                type='Identifier',
                highlight='pink',
                content=symbol,
                endline=endline,
                wikidata_result=json.dumps({'w': wikidata_result}),
                word_window=json.dumps({'word_window': get_word_window(line_num)}),
                #word_window=json.dumps({'word_window': wikidata_result})
                ##word_window=json.dumps({'wordWindow': 'test'})
                arXiv_evaluation_items=json.dumps({'arXiv_evaluation_items': arXiv_evaluation_items}),
                wikipedia_evaluation_items=json.dumps({'wikipedia_evaluation_items': wikipedia_evaluation_items})
            )
        )

    # add the dollar signs back again
    """dollar = Identifier(
        str(uuid1()),
        type='Identifier',
        highlight='yellow',
        content='$',
        endline=False,
        wikidata_result=None,
        word_window=None,
        arXiv_evaluation_items=None,
        wikipedia_evaluation_items=None
        )

    processed_maths_env = [dollar] + processed_maths_env + [dollar]"""

    formula1, formula2 = entire_formula(str(math_env))
    processed_maths_env = [formula1] + processed_maths_env + [formula2]

    return processed_maths_env


def get_math_envs(file):
    tex_soup = TexSoup(file)
    print(tex_soup)
    equation = list(tex_soup.find_all('equation'))
    align = list(tex_soup.find_all('align'))
    dollar = list(tex_soup.find_all('$'))
    math_envs = equation + align + dollar
    print('MATH_ENVS:', math_envs)
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


    global tagger, \
        identifier_retriever, \
        nesparql, mathsparql, \
        arXiv_evaluation_list_handler, \
        wikipedia_evaluation_list_handler
    nesparql = NESparql()
    # mathsparql = MathSparql()
    tagger = NLTK_NER()
    identifier_retriever = RakeIdentifier()
    arXiv_evaluation_list_handler = ArXivEvaluationListHandler()
    wikipedia_evaluation_list_handler = WikipediaEvaluationListHandler()
    #identifier_retriever = SpaceyIdentifier()
    #tagger = Spacy_NER()
    #tagger = StanfordCoreNLP_NER()


    processed_lines = process_lines(request_file)


    return LaTeXFile(processed_lines)
