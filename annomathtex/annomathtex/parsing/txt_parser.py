from ..parsing.parser import Parser
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


class TXTParser(Parser):
    """
    This class is a subclass of the abstract base class Parser. It is used to parse and process text files (including
    wikitext).
    """

    def decode(self, request_file):
        """
        Text files have to be read and decoded.
        :param request_file: The file that the user selected.
        :return: The decoded file as a string.
        """
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

        file = request_file.read()
        file = decode_txt(file)
        return file

    def extract_math_envs(self):
        """
        Extract the math environments that are contained in the file (e.g. within '$...$').
        :return: A list of the math environments as strings.
        """
        ignore = [r'\n', '', r'\s']
        soup = BeautifulSoup(self.file)
        #might work without list()
        # tex parser returns tuple of old,
        # and new math_env, which is why its also necessary to do that here.
        """math_envs = list(
            map(
                lambda math_env: ' '.join(chunk for chunk in math_env.contents if chunk not in ignore),
                list(soup.find_all('math'))
            )
        )"""
        math_envs = [str(tag) for tag in list(soup.find_all('math'))]
        return math_envs

    def extract_tags_to_remove(self):
        """
        If the file is a wikitext, remove certain tags that make the file harder to read (e.g. reference tags).
        :return: A list of the tags that were extracted for removal.
        """
        soup = BeautifulSoup(self.file)
        #tag_list = ['ref', 'sub']
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
        #todo: check time and use more efficient method
        self.file = self.file.replace('<math>', '')
        self.file = self.file.replace('</math>', '')
        print('REMOVE TAGS: {}'.format([str(tag) for tag in self.extract_tags_to_remove()]))
        for tag in self.extract_tags_to_remove():
            print(str(tag))
            self.file = self.file.replace(str(tag), '')

        print(self.file)



