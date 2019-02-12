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


# named_entity_dict is used to store all named entities with the corresponding index in the text
# maths environments are treated as one word
# maths_env_dict is analogous
__named_entitiy_dict = {}
__maths_env_dict = {}

#structure:
#line_num: {nes: ... , identifiers: ...}
__line_dict = {}


def decode(request_file):
    """
    TeX evaluation_files are in bytes and have to be converted to string in utf-8
    :return: list of lines (string)
    """
    bytes = request_file.read()
    string = bytes.decode('utf-8')
    string_split = string.splitlines(1)
    return string_split


def extract_words(line_chunk, endline, line_num):
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
    tagged_words = identifier_retriever.extract_identifiers(line_chunk, endline)

    #add named entities from this line to __line_dict
    __line_dict[line_num] = [word for word in tagged_words if word.named_entity]
    return tagged_words


def entire_formula(line_chunck, endline):
    pass


def extract_identifiers(line_chunk, endline, line_num, word_window_size=3):
    """
    This method should only look at extracting identifiers from the line_chunk.
    Handle the entire formula in another method.
    This method extracts the identifiers that are contained in a line.
    :param line_chunk: Part of line that is being processed (list of words or maths env).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Identifier() objects.
    """
    # todo: different method of splitting
    #identifiers = []
    #identifier_tokens = nltk.word_tokenize(line_chunk)

    #remove dollar signs
    #sympy throws error with them in the formula
    line_chunk = line_chunk.replace('$', '')

    identifiers = FormulaSplitter(line_chunk).get_identifiers()

    split_regex = "|".join(str(i) for i in identifiers)
    split_regex = r"({})".format(split_regex)

    split_line_chunk = re.split(split_regex, line_chunk)


    #word_window = [ne for i in range(line_num-3, line_num+3) for ne in __line_dict[i] if i in __line_dict]
    #todo: nes from neighbouring lines, ranked
    word_window = [ne for ne in __line_dict[line_num]]
    word_window_words = [ne.content for ne in word_window]
    #print(line_chunk, word_window_words)
    print(line_num, line_chunk, __line_dict[line_num])


    processed_maths_env = []
    for symbol in split_line_chunk:
        if symbol in identifiers:
            wikidata_result = mathsparql.broad_search(symbol)
        else:
            wikidata_result = None

        processed_maths_env.append(
            Identifier(
                str(uuid1()),
                type='Identifier',
                highlight='pink',
                content=symbol,
                endline=False,
                wikidata_result=json.dumps({'w': wikidata_result}),
                word_window=word_window
            )
        )



    #add the dollar signs back again
    dollar = Identifier(
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
        processed_maths_env[-1].endline = True


    return processed_maths_env



def process_lines(request_file):
    """
    processes the file
    todo: check runtime with multiprocessing
    :param request_file: request.FILES['file'], the file that the user uploaded
    :return:
    """

    global nesparql, mathsparql, wikidata_search_results
    nesparql = NESparql()
    #mathsparql = MathSparql()
    wikidata_search_results = {} #equal search strings don't have to be repeated


    lines = decode(request_file)
    all_processed_lines = []
    for line_num, line in enumerate(lines):
        line_copy = line
        #print(re.split(r'(\$\$?.+?\$\$?|\s+)', line))
        maths = re.findall(r'\$\$?.+?\$\$?', line)
        processed_line = []
        if len(maths) > 0:
            for i, math in enumerate(maths):
                search_pattern = '.*?(?=\$.+?\$)'
                non_math = re.findall(search_pattern, line_copy)[0]
                processed_line += extract_words(non_math, False, line_num)
                processed_line += extract_identifiers(math, False, line_num)
                line_copy = line[len(non_math) + len(math):]

        if line == '\n':
            processed_line = [EmptyLine(uuid1())]
        else:
            processed_line += extract_words(line_copy, False, line_num)

        all_processed_lines.append(processed_line)



    return all_processed_lines


def get_processed_file(request_file):
    """

    :param request_file:
    :return:
    """
    #possible taggers
    #tagger_names = ['NLTK_NER_1', 'NLTK_NER_2', 'StanfordCoreNLP_NER', 'Spacy_NER']


    global tagger, identifier_retriever
    tagger = NLTK_NER()
    #identifier_retriever = RakeIdentifier()
    identifier_retriever = SpaceyIdentifier()
    #tagger = Spacy_NER()
    #tagger = StanfordCoreNLP_NER()



    processed_lines = process_lines(request_file)

    for k in __line_dict:
        words = [w.content for w in __line_dict[k]]
        print(k, words)
    return LaTeXFile(processed_lines)



