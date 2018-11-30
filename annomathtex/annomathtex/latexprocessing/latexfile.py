import os
import re
from .word import Word
from .chunk import Chunk





class LaTexFile:

    def __init__(self):
        self.title = 'example title'
        self.body = self.find_math_tags()
        #self.body = self.load_file()
        #self.body = self.get_body()

    def get_body(self):

        text = self.load_file()
        highlighting = []
        for i, w in enumerate(text):
            h = False
            if i % 3 == 0:
                h = True
            highlighting.append(Word(w, h))
        return highlighting

    def find_math_tags(self):
        lines = self.load_file()
        processed_lines = []
        for line in lines:
            chunks = []
            line_copy = line
            maths = re.findall(r'\$.*?\$', line)
            #print(line, maths)
            if len(maths) > 0:
                for i, math in enumerate(maths):
                    search_pattern = '.*?(?=\$.*?\$)'
                    non_math = re.findall(search_pattern, line_copy)[0]
                    chunks.append(Chunk(non_math, type='non_math', highlight=False, endline=False))
                    chunks.append(Chunk(math, type='math', highlight=True, endline=False))
                    line_copy = line[len(non_math)+len(math):]

            chunks.append(Chunk(line_copy, type='non_math', highlight=False, endline=True))
            processed_lines.append(chunks)

        #for chunk in chunks:
        #    print(chunk.str, chunk.type, chunk.endline)

        #return chunks
        return processed_lines



    def load_file(self):
        with open(os.getcwd() + '/DJtest/latexfiles/assignment03.tex', 'r') as file:
            lines_string = file.read()

        #for i in lines_string.splitlines():
        #    print(i)
        #print(lines_string.splitlines(1))
        return lines_string.splitlines(1)
