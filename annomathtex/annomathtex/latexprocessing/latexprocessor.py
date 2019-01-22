import re
import nltk
from uuid import uuid1
from .model.word import Word
from .model.identifier import Identifier
from .model.empty_line import EmptyLine
from .model.latexfile import LaTeXFile


class LaTeXProcessor:
    #todo: add colour coding for individual latex commands
    """
    Processes the LaTeX file that the user uploads
    """

    def __init__(self, requestFile):
        """
        :param requestFile: request.FILES['file'], the file that the user uploaded
        """
        self.requestFile = requestFile


    def get_file_string(self):
        """
        For testing purposes
        :return: decoded file (string)
        """
        return self.decode()

    def get_processed_lines(self):
        """
        For testing purposes
        :return: Found Math Tags etc.
        """
        return self.find_math_tags()

    def get_latex_file(self):
        """
        :return: processed LaTeX file with body, chunks, words
        """
        processed_lines = self.find_math_tags()
        return LaTeXFile(processed_lines)


    def decode(self):
        """
        TeX files are in bytes and have to be converted to string in utf-8
        :return: list of lines (string)
        """
        bytes = self.requestFile.read()
        string = bytes.decode('utf-8')
        string_split = string.splitlines(1)
        return string_split


    def find_math_tags(self):
        """
        #TODO: multiline math environments
        Finds the math tags and creates chunks that highlights them
        :return: List of lines of the file
        """

        def extract_words(line_chunk, endline):
            """
            This method extracts the words that are contained in a line.
            :param line_chunk: Part of line that is being processed (list of words).
            :param endline: Boolean. True if the line_chunk ends the line.
            :return: List of the words fom line_chunk as Word() objects.
            """
            #todo: use NECKAR NER
            words= []
            word_tokens = nltk.word_tokenize(line_chunk)

            for _, word in enumerate(word_tokens):
                words.append(Word(str(uuid1()), type='Word', highlight="black", content=word, endline=False, named_entity=False))

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
            #todo: implement
            identifiers = []
            identifier_tokens = nltk.word_tokenize(line_chunk)

            for identifier in identifier_tokens:
                identifiers.append(Identifier(str(uuid1()), type='Identifier', highlight='pink', content=identifier, endline=False, qid=None))

            if endline:
                identifiers[-1].endline = True

            return identifiers

        pattern1 = r'\$\$?.+?\$\$?'
        pattern2 = r'\\\[.*?\\\]'
        pattern3 = r'\\\(.*?\\\)'


        lines = self.decode()
        all_processed_lines = []
        for line in lines:
            line_copy = line
            #maths = re.findall(r'\$.*?\$', line)
            maths = re.findall(r'\$\$?.+?\$\$?', line)
            #maths += re.findall(r'\\\[.*?\\\]', line)
            #maths += re.findall(r'\\\(.*?\\\)', line)
            processed_line = []
            if len(maths) > 0:
                for i, math in enumerate(maths):
                    #search_pattern = '.*?(?=\$.*?\$)'
                    search_pattern = '.*?(?=\$.+?\$)'
                    #what if mulitple math environments per line? Problem?
                    #shouldn't matter, an identifier won't go beyond linebreak
                    non_math = re.findall(search_pattern, line_copy)[0]
                    processed_line += extract_words(non_math, False)
                    processed_line += extract_identifiers(math, False)
                    line_copy = line[len(non_math)+len(math):]

            if line == '\n':
                processed_line = [EmptyLine(uuid1())]
            else:
                processed_line += extract_words(line_copy, False)

            all_processed_lines.append(processed_line)

        #for l in all_processed_lines:
        #    print(l)

        #testing purposes
        #all_processed_lines.insert(20, [Word('identifier', type='Word', highlight="pink", content="TESTWORDBLABLABLA", endline=True, named_entity=True)])

        return all_processed_lines

