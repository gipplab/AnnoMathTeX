from .parser import Parser


class TXTParser(Parser):

    def decode(self, request_file):
        string = request_file.read()
        return string

    def extract_math_envs(self):
