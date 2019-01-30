import re
import nltk
from uuid import uuid1
from .model.word import Word
from .model.identifier import Identifier
from .model.empty_line import EmptyLine
from .model.latexfile import LaTeXFile
from .named_entity_handling import NESparql
from .math_environment_handling import MathSparql
from .named_entity_recognition import NLTK_NER, StanfordCoreNLP_NER, Spacy_NER
from .identifier_retrieval import RakeIdentifier, SpaceyIdentifier
import json
import time


def decode(request_file):
    """
    TeX files are in bytes and have to be converted to string in utf-8
    :return: list of lines (string)
    """
    bytes = request_file.read()
    string = bytes.decode('utf-8')
    string_split = string.splitlines(1)
    return string_split


def extract_words(line_chunk, endline):
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
    cutoff = 7.0
    #for RAKE
    tagged_words = identifier_retriever.extract_identifiers(line_chunk, endline, cutoff)
    #for Spacey
    #tagged_words = identifier_retriever.extract_identifiers(line_chunk, endline)
    return tagged_words


def extract_identifiers(line_chunk, endline):
    """
    This method extracts the identifiers that are contained in a line.
    :param line_chunk: Part of line that is being processed (list of words).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Identifier() objects.
    """
    # todo: different method of splitting
    identifiers = []
    identifier_tokens = nltk.word_tokenize(line_chunk)

    for identifier in identifier_tokens:

        if identifier not in wikidata_search_results:
            wikidata_result = mathsparql.broad_search(identifier)
            wikidata_search_results[identifier] = wikidata_result

        else:
            wikidata_result = wikidata_search_results[identifier]

        #wikidata_result = json.dumps(mathsparql.broad_search(identifier))

        #print('wikidata results: ', wikidata_result)
        #if len(wikidata_result)>0:
        #    wikidata_result = {'0': {'01':'test01'}}

        identifiers.append(
            Identifier(
                str(uuid1()),
                type='Identifier',
                highlight='pink',
                content=identifier,
                endline=False,
                wikidata_result = json.dumps({'w': wikidata_result})
            )
        )

    if endline:
        identifiers[-1].endline = True

    return identifiers



def process_lines(request_file):
    """
    processes the file
    todo: check runtime with multiprocessing
    :param request_file: request.FILES['file'], the file that the user uploaded
    :return:
    """

    global nesparql, mathsparql, wikidata_search_results
    nesparql = NESparql()
    mathsparql = MathSparql()
    wikidata_search_results = {} #equal search strings don't have to be repeated


    lines = decode(request_file)
    all_processed_lines = []
    for line in lines:
        line_copy = line
        maths = re.findall(r'\$\$?.+?\$\$?', line)
        processed_line = []
        if len(maths) > 0:
            for i, math in enumerate(maths):
                search_pattern = '.*?(?=\$.+?\$)'
                non_math = re.findall(search_pattern, line_copy)[0]
                processed_line += extract_words(non_math, False)
                processed_line += extract_identifiers(math, False)
                line_copy = line[len(non_math) + len(math):]

        if line == '\n':
            processed_line = [EmptyLine(uuid1())]
        else:
            processed_line += extract_words(line_copy, False)

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
    identifier_retriever = RakeIdentifier()
    #identifier_retriever = SpaceyIdentifier()
    #tagger = Spacy_NER()
    #tagger = StanfordCoreNLP_NER()



    processed_lines = process_lines(request_file)
    return LaTeXFile(processed_lines)



