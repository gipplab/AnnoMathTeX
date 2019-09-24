from ..parsing.parser import Parser
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")
from ..views.data_repo_handler import DataRepoHandler


class WikipediaParser(Parser):
    """
    This class is a subclass of the abstract base class Parser. It is used to parse and process wikitext.
    """
    def decode(self, wikipedia_article):
        file = wikipedia_article.decode()
        def decode_txt(f, encoding="ascii", errors="ignore"):
            """
            Decoding unique to txt files. Encode to ascii and ignore all errors. Only very few characters aren't
            recognised, and the entire file can still be loaded even if an error arrises.
            :param f: The file that has been loaded into memory and read (string).
            :param encoding: The desired encoding, ascii for now.
            :param errors: How to handle errors, ignore for now.
            :return: the decoded txt file.
            """
            return f.decode(encoding=encoding, errors=errors)


        return file

    def extract_math_envs(self):
        """
        Extract the math environments that are contained in the file (e.g. within '$...$').
        :return: A list of the math environments as strings.
        """
        ignore = [r'\n', '', r'\s']
        soup = BeautifulSoup(self.file)

        def remove_special_chars(math_env):
            math_env = math_env.replace('amp;', '')
            return math_env

        math_envs = [remove_special_chars(str(tag)) for tag in list(soup.find_all('math'))]
        self.__LOGGER__.debug(math_envs)
        return math_envs

    def extract_tags_to_remove(self):
        """
        If the file is a wikitext, remove certain tags that make the file harder to read (e.g. reference tags).
        :return: A list of the tags that were extracted for removal.
        """
        soup = BeautifulSoup(self.file)
        tag_list = ['ref']
        tags = list(soup.find_all(tag_list))
        return tags

    def remove_tags(self):
        """
        Remove <math> tags (content is encapsulated by '$...$').
        Remove tags like <ref> ... completely since they only mess up ne recognition and add no value to file.
        UPDATE: NE recognition works well with the tags still in the file, still the readability is greatly improved by
                removing these tags.
        :return: None, the class attribute file is changed directly.
        """
        self.file = self.file.replace('<math>', '')
        self.file = self.file.replace('</math>', '')
        for tag in self.extract_tags_to_remove():
            print(str(tag))
            self.file = self.file.replace(str(tag), '')

    def remove_math_tags(self, line):
        line = line.replace('<math>', '')
        line = line.replace('</math>', '')
        return line

    def file_to_json(self):
        """
        Needed for frontend rendering. Selection of wikipedia article is done through ajax.
        Can't send python class file directly to javascript and ajax can't end in django template.
        :return:
        """
        pass




