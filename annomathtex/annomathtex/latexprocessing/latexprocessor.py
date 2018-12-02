import re
from .model.chunk import Chunk
from .model.word import Word





class LaTeXProcessor:

    def __init__(self, requestFile):
        """
        :param requestFile: request.FILES['file'], the file that the user uploaded
        """
        self.requestFile = requestFile


    def get_file_string(self):
        return self.decode(self.requestFile)

    def get_processed_lines(self):
        return self.find_math_tags(self.file_string)


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
        lines = self.load_file()
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

