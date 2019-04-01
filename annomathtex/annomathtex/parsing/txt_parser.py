from ..parsing.parser import Parser
from bs4 import BeautifulSoup
import logging
import warnings
warnings.filterwarnings("ignore")


class TXTParser(Parser):

    def decode2(self, s, encoding="ascii", errors="ignore"):
        return s.decode(encoding=encoding, errors=errors)

    def decode(self, request_file):
        #with open(request_file, 'rb') as f:
        #    bytes = request_file.read()
        #string = bytes.decode()
        #self.__LOGGER__.info('decode', type(string))
        file = request_file.read()
        #file = file.decode('ascii')
        #file = file.decode('utf-8')
        file = self.decode2(file)
        return file

    def extract_math_envs(self):
        ignore = [r'\n', '', r'\s']
        soup = BeautifulSoup(self.file)
        #might work without list()
        #todo: handle special characters,
        # tex parser returns tuple of old,
        # and new math_env, which is why its also necessary here
        math_envs = list(
            map(
                lambda math_env: (' '.join(chunk for chunk in math_env.contents if chunk not in ignore),
                                  ' '.join(chunk for chunk in math_env.contents if chunk not in ignore)),
                list(soup.find_all('math'))
            )
        )
        return math_envs


