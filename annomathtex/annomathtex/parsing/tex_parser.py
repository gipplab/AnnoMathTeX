from .parser import Parser
from TexSoup import TexSoup
import logging
import re
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

        def handle_special_chars(math_env):
            special_char = re.search(r'_(\w|\d)', math_env)
            if special_char:
                found_char = re.search(r'(?<=_)(\w|\d)', math_env).group()[0]
                found_char_with_brackets = '{' + found_char + '}'
                math_env_new = math_env.replace(found_char, found_char_with_brackets)
                #math_env_new = math_env_new.replace('(', '')
                #math_env_new = math_env_new.replace(')', '')
                self.__LOGGER__.debug(' found special CHARS: {}'.format(found_char))
                self.__LOGGER__.debug(' contains special CHAR --- math_env_old: {} ---- math_env_new: {}'.format(math_env, math_env_new))
                return (math_env, math_env_new)
            return (math_env, math_env)

        tex_soup = TexSoup(self.file)
        equation = list(tex_soup.find_all('equation'))
        align = list(tex_soup.find_all('align'))
        dollar = list(tex_soup.find_all('$'))
        math_envs = equation + align + dollar
        #math_envs = list(map(lambda m: str(m), math_envs))
        math_envs = list(map(lambda m: handle_special_chars(str(m)), math_envs))

        self.__LOGGER__.info(' extracted math_envs: {}'.format(math_envs))
        return math_envs
