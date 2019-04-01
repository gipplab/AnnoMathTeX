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

    def extract_tags_to_remove(self):
        soup = BeautifulSoup(self.file)
        #tag_list = ['ref', 'sub']
        tag_list = ['ref']
        tags = list(soup.find_all(tag_list))
        return tags

    def remove_tags(self):
        """
        remove <math> tags (content is encapsulated by $
        remove tags like <ref> ... completely since they only mess up ne recognition and add no value to file
        :return:
        """
        #todo: check time and use more efficient method
        self.file = self.file.replace('<math>', '')
        self.file = self.file.replace('</math>', '')
        print('REMOVE TAGS: {}'.format([str(tag) for tag in self.extract_tags_to_remove()]))
        for tag in self.extract_tags_to_remove():
            print(str(tag))
            self.file = self.file.replace(str(tag), '')



