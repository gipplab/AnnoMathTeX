import re
import nltk
from uuid import uuid1
from .model.word import Word
from .model.identifier import Identifier
from .model.empty_line import EmptyLine
from .model.latexfile import LaTeXFile
from .named_entity_handling import NESparql
from .math_environment_handling import MathSparql
import json


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
    :param line_chunk: Part of line that is being processed (list of words).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Word() objects.
    """
    # todo: use NECKAR NER to evaluate later, evaluation can be done in different file (independent of Django)

    words = []
    word_tokens = nltk.word_tokenize(line_chunk)

    #print(word_tokens)

    for _, word in enumerate(word_tokens):
        words.append(
            Word(
                str(uuid1()),
                type='Word',
                highlight="black",
                content=word,
                endline=False,
                named_entity=False,
                wikidata_result = None
            )
        )

    if endline:
        words[-1].endline = True

    return words


def extract_identifiers(line_chunk, endline):
    """
    This method extracts the identifiers that are contained in a line.
    :param line_chunk: Part of line that is being processed (list of words).
    :param endline: Boolean. True if the line_chunk ends the line.
    :return: List of the words fom line_chunk as Identifier() objects.
    """
    # todo: implement
    identifiers = []
    identifier_tokens = nltk.word_tokenize(line_chunk)

    for identifier in identifier_tokens:

        wikidata_result = mathsparql.broad_search(identifier)
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
                wikidata_result= json.dumps({'wikidata_result':wikidata_result})
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

    global nesparql, mathsparql
    nesparql = NESparql()
    mathsparql = MathSparql()


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
    processed_lines = process_lines(request_file)
    return LaTeXFile(processed_lines)



