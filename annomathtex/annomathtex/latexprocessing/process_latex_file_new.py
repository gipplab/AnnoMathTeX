import re
from uuid import uuid1
from .model.identifier import Identifier
from .model.formula import Formula
from .model.empty_line import EmptyLine
from .model.latexfile import LaTeXFile
from .named_entity_handling import NESparql
from .named_entity_recognition import NLTK_NER
from .identifier_retrieval import RakeIdentifier
from .evaluation_list_handling import ArXivEvaluationListHandler, WikipediaEvaluationListHandler
import json
from .latexformlaidentifiers import FormulaSplitter
from TexSoup import TexSoup
from ..config import recommendations_limit

__line_dict__ = {}
#contains all the NEs and Identifiers that have been found
#used to reference annotated items, so that they only have to be annotated once for whole document
__linked_words__ = {}
__linked_math_symbols__ = {}
__line_dict__2 = {}

def decode(request_file):
    """
    TeX evaluation_files are in bytes and have to be converted to string in utf-8
    :return: list of lines (string)
    """
    bytes = request_file.read()
    string = bytes.decode('utf-8')
    #string_split = string.splitlines(1)
    print('TYPE OF VARIABLE STRING IS {}'.format(type(string)))
    return string


def form_word_links(tagged_words):
    for word in tagged_words:
        if word.named_entity and word.content:
            if word.content in __linked_words__:
                __linked_words__[word.content].append(word.unique_id)
            else:
                __linked_words__[word.content] = [word.unique_id]


def form_symbol_links(symbol):
    if symbol.content:
        if symbol.content in __linked_math_symbols__:
            __linked_math_symbols__[symbol.content].append(symbol.unique_id)
        else:
            __linked_math_symbols__[symbol.content] = [symbol.unique_id]


def form_formula_links(formula1, formula2):
    math_env = formula1.math_env
    if math_env:
        if math_env in __linked_math_symbols__:
            __linked_math_symbols__[math_env] += [formula1.unique_id, formula2.unique_id]
        else:
            __linked_math_symbols__[math_env] = [formula1.unique_id, formula2.unique_id]






def extract_words(sentence, line_num):
    """
    This method extracts the words that are contained in a line.
    If a named entity is contained, mark that.
    :param line_chunk: Part of line that is being processed (list of words).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Word() objects.
    """
    #select between NE tagging and keyword extraction
    #todo: adjust newline in all taggers and identifier retrievers
    tagged_words = tagger.tag(sentence)
    #for RAKE & Spacey
    #tagged_words = identifier_retriever.extract_identifiers(sentence)

    form_word_links(tagged_words)

    """sun = list(filter(lambda x: x.content=='Sun', tagged_words))

    if len(sun) > 0:
        sun = sun[0]
        i = tagged_words.index(sun)
        sun.unique_id = 'SUNID'
        tagged_words[i] = sun"""



    __line_dict__[line_num] = [word for word in tagged_words if word.named_entity]

    #for word in tagged_words:
    #    if word.named_entity:
    #        __line_dict__2[__index__] = (word.content, word.unique_id)
    #    __index__ += 1





    return tagged_words




def get_word_window(line_num):
    #todo: make class, to be consistent
    #word_window = [__line_dict__[n] for ]
    word_window = []
    limit = int(recommendations_limit/2)
    line_nums = range(line_num-limit,line_num+limit)
    #print('LINENUMS: ', list(line_nums), ' LINE: ', line_num)
    #for n in [line_num, line_num-1, line_num+1, line_num-2, line_num+2]:
    """for n in line_nums:
        if n in __line_dict__:
            for word in __line_dict__[n]:
                word_window.append({
                    'content': word.content,
                    'unique_id': word.unique_id
                })"""

    i = 0
    while i < recommendations_limit:
        #lines before
        b = line_num - i
        #lines after
        a = line_num + i

        if b in __line_dict__:
            for word in reversed(__line_dict__[b]):
                #value not yet in word window
                if not list(filter(lambda d: d['content'] == word.content, word_window)):
                    word_window.append({
                        'content': word.content,
                        'unique_id': word.unique_id
                    })
                    i+=1
        if a in __line_dict__:
            for word in reversed(__line_dict__[a]):
                #value not yet in word window
                if not list(filter(lambda d: d['content'] in word.content, word_window)):
                    word_window.append({
                        'content': word.content,
                        'unique_id': word.unique_id
                    })
        i+=1





    if not word_window:
        word_window = [{}]

    return word_window[:10]


def entire_formula(math_env, line_num):

    #todo: put this in external class -> consistency

    #for some reason django
    #math_env = math_env.replace('=', '__EQUALS__')


    formula1 = Formula(
        str(uuid1()),
        type='Formula',
        highlight='yellow',
        content='$',
        endline=False,
        wikidata_result=None,
        word_window=json.dumps({'word_window': get_word_window(line_num)}),
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
        word_window=json.dumps({'word_window': get_word_window(line_num)}),
        arXiv_evaluation_items=None,
        wikipedia_evaluation_items=None,
        math_env=math_env
    )


    form_formula_links(formula1, formula2)

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


    identifiers = FormulaSplitter(math_env).get_identifiers()

    try:
        split_regex = "|".join(str(i) for i in identifiers)
        split_regex = r"({})".format(split_regex)
        split_math_env = re.split(split_regex, math_env)
    except Exception:
        split_math_env = math_env


    processed_maths_env = []
    for symbol in split_math_env:

        if identifiers and symbol in identifiers:
            #wikidata_result = mathsparql.broad_search(symbol)
            wikidata_result=None
            arXiv_evaluation_items = arXiv_evaluation_list_handler.check_identifiers(symbol)
            wikipedia_evaluation_items = wikipedia_evaluation_list_handler.check_identifiers(symbol)
        else:
            wikidata_result = None
            arXiv_evaluation_items =None
            wikipedia_evaluation_items =None

        endline = True if symbol == '\n' else False

        id_symbol = Identifier(
                str(uuid1()),
                type='Identifier',
                highlight='pink',
                content=symbol,
                endline=endline,
                wikidata_result=json.dumps({'w': wikidata_result}),
                word_window=json.dumps({'word_window': get_word_window(line_num)}),
                arXiv_evaluation_items=json.dumps({'arXiv_evaluation_items': arXiv_evaluation_items}),
                wikipedia_evaluation_items=json.dumps({'wikipedia_evaluation_items': wikipedia_evaluation_items})
            )

        processed_maths_env.append(id_symbol)
        form_symbol_links(id_symbol)

    # add the dollar signs back again
    formula1, formula2 = entire_formula(str(math_env), line_num)
    processed_maths_env = [formula1] + processed_maths_env + [formula2]

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
    :param request_file: request.FILES['file'], the file that the user uploaded
    :return:
    """

    file = decode(request_file)
    #file = request_file
    math_envs = get_math_envs(file)

    #math_envs = []

    for i, m in enumerate(math_envs):
        try:
            file = file.replace(m, '__MATH_ENV__', 1)
        except Exception as e:
            print(e)
            continue


    lines = [p for p in file.split('\n')]

    processed_lines = [extract_words(s, i) for i,s in enumerate(lines)]

    processed_sentences_including_maths = []
    for line_num, line in enumerate(processed_lines):
        line_new = []
        if len(line) < 1:
            line_new.append(EmptyLine(uuid1()))
        for w in line:
            if re.search(r'__MATH_ENV__', w.content):
                math_env = math_envs[0]
                math_envs.pop(0)
                #line_new.append(extract_identifiers(math_env, line_num))
                foo = extract_identifiers(math_env, line_num)
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
        wikipedia_evaluation_list_handler, \
        __index__
    nesparql = NESparql()
    # mathsparql = MathSparql()
    tagger = NLTK_NER()
    identifier_retriever = RakeIdentifier()
    arXiv_evaluation_list_handler = ArXivEvaluationListHandler()
    wikipedia_evaluation_list_handler = WikipediaEvaluationListHandler()
    __index__ = 0
    #identifier_retriever = SpaceyIdentifier()
    #tagger = Spacy_NER()
    #tagger = StanfordCoreNLP_NER()


    processed_lines = process_lines(request_file)
    return LaTeXFile(processed_lines, __linked_words__, __linked_math_symbols__)
