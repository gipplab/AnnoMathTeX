from .parser import Parser
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


class TXTParser(Parser):

    def decode(self, request_file):
        #with open(request_file, 'rb') as f:
        #    bytes = request_file.read()
        #string = bytes.decode()
        #self.__LOGGER__.info('decode', type(string))
        file = request_file.read()
        return file.decode('ascii')

    def extract_math_envs(self):
        ignore = [r'\n', '', r'\s']
        soup = BeautifulSoup(self.file)
        #might work without list()
        math_envs = list(
            map(
                lambda math_env: ' '.join(chunk for chunk in math_env.contents if chunk not in ignore),
                list(soup.find_all('math'))
            )
        )
        return math_envs


