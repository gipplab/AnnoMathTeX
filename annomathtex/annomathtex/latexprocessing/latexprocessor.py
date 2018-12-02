import re
from .model.chunk import Chunk
from .model.word import Word
from .model.latexfile import LaTeXFile


class LaTeXProcessor:
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
        File is in bytes and has to be converted to string in utf-8
        :return: list of lines (string)
        """
        bytes = self.requestFile.read()
        string = bytes.decode('utf-8')
        string_split = string.splitlines(1)
        return string_split


    def find_math_tags(self):
        """
        Finds the math tags and creates chunks that hihglights them
        :return: List of lines of the file
        """
        lines = self.decode()
        processed_lines = []
        for line in lines:
            chunks = []
            line_copy = line
            maths = re.findall(r'\$.*?\$', line)
            if len(maths) > 0:
                for i, math in enumerate(maths):
                    search_pattern = '.*?(?=\$.*?\$)'
                    non_math = re.findall(search_pattern, line_copy)[0]
                    chunks.append(Chunk(non_math, type='non_math', highlight=False, endline=False))
                    chunks.append(Chunk(math, type='math', highlight=True, endline=False))
                    line_copy = line[len(non_math)+len(math):]

            chunks.append(Chunk(line_copy, type='non_math', highlight=False, endline=True))
            processed_lines.append(chunks)

        return processed_lines


    def find_named_entities(self):
        #todo
        pass

