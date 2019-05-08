from annomathtex.annomathtex.recommendation.sparql import Sparql
from annomathtex.annomathtex.recommendation.sparql_queries import identifier_query
from bs4 import BeautifulSoup
import json
import os
import re

import warnings
warnings.filterwarnings("ignore")

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
        self.greek_letters_path = os.getcwd() + '/annomathtex/annomathtex/parsing/mathhandling/latex_math_symbols.json'

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
        all_symbols = [s.replace('\\', '\\\\') for key in keys for s in all_dict[key]]
        all_symbols_string = '|'.join(all_symbols)
        all_symbols_string = r'({})'.format(all_symbols_string)
        return all_symbols_string

    def get_greek_letters(self, path):
        """
        Load the extracted file of latex symbols, and more specifically the greek letters. Needed for the extraction
        of identifiers. The greek letters are written as: 'alpha, 'beta', ...
        :param path: The path to the file of latex symbols.
        :return: A regular expression that allows extraction of all greek letters from a string
        """
        with open(path, 'r') as f:
            s = f.read()

        all_dict = json.loads(s)
        greek_letters = all_dict['greek_letters']
        greek_letters_set = set(map(lambda g: g[1:].lower(), greek_letters))
        greek_letters_regex = r'|'.join(g for g in greek_letters_set)
        return greek_letters_regex

    def get_id_pos_len(self):
        """
        This method extracts the identifiers from a math environment using a regex. In addition the position of each identifier
        and it's length is added to a triple, which is used in get_split_math_env() to split the entire math
        environment into the identifiers and non identifier parts.
        :return: A triple of the identifier, the position of the identifier in the string and the length of the
                 identifier.
        """

        def remove_math_tags(math_env):
            math_env = math_env.replace('<math>', '')
            math_env = math_env.replace('</math>', '')
            return math_env

        greek_letters_regex = self.get_greek_letters(self.greek_letters_path)
        identifier_r = r'(\b[a-z]\b|(?<=_)[a-z]|(?<=[^a-z])[a-z](?=_)|{})'.format(greek_letters_regex)
        #identifier_r = r'(\b[a-z]\b|(?<=_)[a-z]|(?<=[^a-z])[a-z](?=_))'
        r = re.compile(identifier_r, re.IGNORECASE)
        self.math_env = remove_math_tags(self.math_env)
        id_pos_len = [(i.group(), i.start(), len(i.group())) for i in r.finditer(self.math_env)]
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
            #formula_chunk = formula_chunk.replace('\\', '\\\\')
            split_math_env.append(formula_chunk)
            split_math_env.append(id)
            identifiers.append(id)
            last_pos = p+l

        end_chunk = self.math_env[last_pos:]
        split_math_env.append(end_chunk)
        return identifiers

class MathSparql(Sparql):
    """
    This class handles all math environment related queries to Wikidata. It inherits from the Sparql class, which
    contains most of the functionality necessary for accessing the Wikidata Query Service API.
    """


    def identifier_search(self, search_string):
        """
        Method used at the moment when the user mouse clicks an identifiers.
        This method searches for the identifiers in the "has par" property of wikidata items.
        :param search_string: The string that is being queried for.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """

        results_list = self.query(identifier_query, search_string, limit=1000)
        return results_list



def extract_math_envs(file):
    """
    Extract the math environments that are contained in the file (e.g. within '$...$').
    :return: A list of the math environments as strings.
    """
    soup = BeautifulSoup(file)
    def remove_special_chars(math_env):
        math_env = math_env.replace('amp;', '')
        return math_env
    math_envs = [remove_special_chars(str(tag)) for tag in list(soup.find_all('math'))]
    return math_envs


def read_file(file_path):
    """
    Text files have to be read and decoded.
    :param request_file: The file that the user selected.
    :return: The decoded file as a string.
    """

    with open(file_path, 'rb') as infile:
        file = infile.read()
    #file = decode_txt(file)
    return file

if __name__ == '__main__':
    eval_files_path = os.getcwd() + '/evaluation/'
    evaluation_files_folder = os.getcwd() + '/annomathtex/annomathtex/recommendation/evaluation_files/'
    files = ['Quantum_harmonic_oscillator.txt', 'K-means clustering.txt', 'symbols.txt']


    all_identifiers = []
    for file in files:
        file_path = eval_files_path + file
        decoded_file = read_file(file_path)
        math_envs = extract_math_envs(decoded_file)

        identifiers = [
                 identifier
                 for math_env in math_envs
                 for identifier in CustomMathEnvParser(math_env).get_split_math_env()
             ]

        all_identifiers += identifiers


    all_identifiers = set(all_identifiers)

    all_results = {}
    i = 0
    for identifier in all_identifiers:
        wikidata_results = MathSparql().identifier_search(identifier)
        all_results[identifier] = wikidata_results
        i += 1

    with open(evaluation_files_folder + 'wikidata.json', 'w') as outfile:
        json.dump(all_results, outfile)





