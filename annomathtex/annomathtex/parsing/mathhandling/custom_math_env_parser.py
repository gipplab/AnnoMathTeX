import json
import re
import string
import os
from ...settings.common import PROJECT_ROOT


class CustomMathEnvParser:
    """
    This class is used to extract the identifiers from a formula and split the formula into parts.
    E.g. the formula 'm ^{( t +1)}_ i' would be split into ['m', ' ^{( ', 't', ' +1)}_ ', 'i] with 'm', 't', and 'i'
    being the identifiers and the rest of the string being symbols that will not be highlighted.
    """

    def __init__(self, math_env):
        """
        :param math_env: The math environment that is being parsed.
        """
        self.math_env = math_env
        self.greek_letters_path = os.path.join(PROJECT_ROOT, 'annomathtex', 'parsing', 'mathhandling', 'latex_math_symbols.json')
        #testing
        #self.greek_letters_path_testing = os.path.join(os.getcwd(), 'latex_math_symbols.json')
        #self.greek_letters_path = self.greek_letters_path_testing

    def load_math_symbols(self, path):
        """
        Not used right now. latex_math_symbols.json is a file that contains a lot of latex commands. The idea was to
        use those to split the math environment. However, I took a different approache now: Extracting the identifiers
        and splitting the math environemnt on those.
        :return: A string of all symbols contained in latex_math_symbols.json that can be used as a regex to split the
                 math environment.
        """
        with open(path, 'r') as f:
            s = f.read()

        all_dict = json.loads(s)
        keys = list(all_dict.keys())
        keys.remove('greek_letters')
        #print(keys)
        all_symbols = [s.replace('\\', '\\\\') for key in keys for s in all_dict[key]]
        all_symbols_string = '|'.join(all_symbols)
        all_symbols_string = r'(?:{})'.format(all_symbols_string)
        return all_symbols_string

    def get_greek_letters(self, path):
        with open(path, 'r') as f:
            s = f.read()

        all_dict = json.loads(s)
        greek_letters = all_dict['greek_letters']
        greek_letters_set = set(map(lambda g: g[1:].lower(), greek_letters))
        greek_letters_regex = r'|'.join(g for g in greek_letters_set)
        return greek_letters_regex


    def split_double_chars(self, id_pos_len):

        id_pos_len_new = []

        for i, item in enumerate(id_pos_len):
            id, pos, l = item
            if l == 2:

                id_1 = id[0]
                pos_1 = pos
                l_1 = 1

                id_2 = id[1]
                pos_2 = pos+1
                l_2 = 1


                #print(id_1, id_2)

                id_pos_len_1 = (id_1, pos_1, l_1)
                id_pos_len_2 = (id_2, pos_2, l_2)

                print(1, id_pos_len)
                print(2, id_pos_len[:i])
                print(3, id_pos_len_1)
                print(4, id_pos_len_2)
                print(5, id_pos_len[i+1:])

                id_pos_len = id_pos_len[:i] + [id_pos_len_1, id_pos_len_2] + id_pos_len[i+1:]

        return id_pos_len




    def get_id_pos_len(self):
        """
        This method extracts the identifiers from a math environment using a regex. In addition the position of each identifier
        and it's length is added to a triple, which is used in get_split_math_env() to split the entire math
        environment into the identifiers and non identifier parts.
        :return: A triple of the identifier, the position of the identifier in the string and the length of the
                 identifier.
        """

        def remove_math_tags(math_env):
            #math_env = math_env.replace('<math>', '')
            math_env = re.sub('<math.*?>', '', math_env)
            math_env = math_env.replace('</math>', '')
            return math_env

        greek_letters_regex = self.get_greek_letters(self.greek_letters_path)
        math_symbols_regex = self.load_math_symbols(self.greek_letters_path)
        identifier_r = r'(\b[a-z]{{1,2}}\b|(?<=_)[a-z]|(?<=[^a-z])[a-z](?=_)|\b[a-z]{{1,2}}(?=_)|{})'.format(greek_letters_regex)
        #identifier_r = r'{}({}|[a-z]{{1,2}})'.format(greek_letters_regex, math_symbols_regex)
        r = re.compile(identifier_r, re.IGNORECASE)
        self.math_env = remove_math_tags(self.math_env)
        #id_pos_len = [(i.group(), i.start(), len(i.group())) for i in r.finditer(self.math_env)]

        id_pos_len = []

        for i in r.finditer(self.math_env):

            id = i.group()
            pos = i.start()
            _len = len(id)

            if _len == 2:
                id_pos_len.append((id[0], pos, 1))
                id_pos_len.append((id[1], pos+1, 1))
            else:
                id_pos_len.append((id, pos, _len))

        #post processed: split 2 char identifiers (e.g. dx)
        #id_pos_len_pp = self.split_double_chars(id_pos_len)
        return id_pos_len


    def get_split_math_env(self):
        """

        This mehtod splits the entire math environemnt the identifier and non identifier parts. These are used in the
        Parser class to construct Identifier and Formula Objects from the math environment.
        :return: The identifiers as a list and the entire math environment (also containing the identifiers) as a list.
        """
        id_pos_len = self.get_id_pos_len()
        split_math_env = []
        identifiers = []
        last_pos = 0
        for id, p, l in id_pos_len:
            formula_chunk = self.math_env[last_pos:p]
            split_math_env.append(formula_chunk)
            split_math_env.append(id)
            identifiers.append(id)
            last_pos = p+l

        end_chunk = self.math_env[last_pos:]
        split_math_env.append(end_chunk)
        return identifiers, split_math_env




def test():
    ex1 = "\,v=dx^{(4)}/dt"  # dx and dt don't get recognized
    ex2 = "E_r^2 - (pc)^2 &= (m_0 c^2)^2"   # pc
    ex3 = "E_r = pc"   # E and pc
    ex4 = "m_0 = 0"    # m

    # regexes:
    # 1: simple variable: \b[a-z]\b

    s = CustomMathEnvParser(ex1)
    #m = s.load_math_symbols(s.greek_letters_path_testing)
    g = s.get_id_pos_len()
    #m = s.load_math_symbols(s.greek_letters_path_testing)
    print(g)


if __name__ == "__main__":
    """
    Used for testing purposes
    """
    test()

