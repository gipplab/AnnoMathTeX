from .parser import Parser
from TexSoup import TexSoup
import warnings
warnings.filterwarnings("ignore")

class TEXParser(Parser):

    def decode2(self, s, encoding="ascii", errors="ignore"):
        return s.decode(encoding=encoding, errors=errors)

    def decode(self, request_file):
        """
        TeX evaluation_files are in bytes and have to be converted to string in utf-8
        :return: list of lines (string)
        """
        bytes = request_file.read()
        string = bytes.decode('utf-8')
        # string_split = string.splitlines(1)
        self.__LOGGER__.debug('TYPE OF VARIABLE STRING IS {}'.format(type(string)))
        return string

    def extract_math_envs(self):
        tex_soup = TexSoup(self.file)
        equation = list(tex_soup.find_all('equation'))
        align = list(tex_soup.find_all('align'))
        dollar = list(tex_soup.find_all('$'))
        math_envs = equation + align + dollar
        return list(map(lambda m: str(m), math_envs))
