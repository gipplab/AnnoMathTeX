import re
import logging
import json
from os import listdir
from uuid import uuid1
from abc import ABCMeta, abstractmethod
from ..parsing.nehandling.named_entity_recognition import NLTK_NER
from ..models.identifier import Identifier
from ..models.formula import Formula
from ..models.empty_line import EmptyLine
from ..models.file import File
from ..recommendation.arxiv_evaluation_handler import ArXivEvaluationListHandler
from ..recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from ..parsing.mathhandling.custom_math_env_parser import CustomMathEnvParser
from ..views.data_repo_handler import DataRepoHandler
from ..config import *


class Parser(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need to parse different input formats (tex, txt, html).
    """

    def __init__(self, request_file, file_name):
        """
        :param request_file: The file that the user selects to annotate.
        :param file_type: The type of the file (tex, txt, html).
        """
        print('in Parser, file_name: {}'.format(file_name))
        logging.basicConfig(level=logging.INFO)
        self.__LOGGER__ = logging.getLogger(__name__)
        self.tagger = NLTK_NER()
        self.file = self.decode(request_file)
        self.file_name = file_name
        self.file_type = file_name.split('.')[-1]
        self.math_envs = self.extract_math_envs()
        self.arXiv_evaluation_list_handler = ArXivEvaluationListHandler()
        self.wikipedia_evaluation_list_handler = WikipediaEvaluationListHandler()
        #dictionary identifier ids and the line they're on
        #needed for word window in file_upload_view
        self.identifier_line_dict = {}

    @abstractmethod
    def decode(self, request_file):
        """
        Decode the file that the user selected. I.e. read it and turn it into a string that can be processed.
        :param request_file: File that the user selected.
        :return: Decoded file (as string).
        """
        raise NotImplementedError('Method decode must be implemented')

    @abstractmethod
    def extract_math_envs(self):
        """
        Extract the math environments from the file. E.g. for wikitext anything within <math> </math>
        :return: The extracted math environments
        """
        raise NotImplementedError('Function extract_math_envs() must be implemented')

    def remove_special_chars(self):
        """
        remove things like <href ....>
        #Not necessary atm.
        :return:
        """
        pass

    def read_annotation_file(self):
        """
        If the user has worked on annotating the same file before, the annotations are stored in a json file.
        This method reads said json file when the user selects the document he wants to annotate.
        :return: Dictionary of existing annoations.
        """
        annotation_file_name = create_annotation_file_name(self.file_name)
        file_path = os.path.join(evaluation_annotations_path, annotation_file_name)
        print('READ ANNOTATOIN FILE: ', annotation_file_name)
        print('IN: ', listdir(evaluation_annotations_path))
        if annotation_file_name in listdir(evaluation_annotations_path):
            with open(file_path, 'r') as f:
                json_annotations =json.load(f)
            self.__LOGGER__.debug('ANNOTATIONS: {}'.format(json_annotations))
            return json_annotations

    def get_annotation_file_from_repo(self):
        return DataRepoHandler().get_annotation_file(self.file_name)

    def remove_math_envs(self):
        """
        Remove all the math environments, process file without them and add them back later
        :return: File without math environments ('__MATH_ENV__' in place of each math_environment)
        """
        for i, m in enumerate(self.math_envs):
            math_env = m
            self.__LOGGER__.debug(' in remove_math_envs() current math_env: {}'.format(m))
            try:
                self.file = self.file.replace(math_env, ' __MATH_ENV__ ', 1)
            except Exception as e:
                self.__LOGGER__.error('math_env {} couldnt be replaced: {}'.format(math_env, e))
                continue


    def form_links(self, processed_lines_unique_ids):
        """
        Create dictionaries of the words and math symbols that appear multiple times in the document. Necessary for
        global annotations. This is used later when annotating a file, to only have to annotate an
        identifier/word once. All the other identical identifiers/words in the file will be annotated automatically
        with the same field. The linked identifier are stored in the class dictionary linked_math_symbols allong with the
        linked formulae. They are stored together, to allow a math environment with only one identifier to be
        treated the same way as an identifier within a math environemnt (e.g. $E$ is treated the same way as
        'E' in $E=mc2$).
        :param processed_lines_unique_ids: The lines of the file that have been processed by the parser. Contain the
        custom generated unique_ids as well.
        :return: Dictionary of linked words, dictionary of linked math symbols.
        """

        words = {}
        math_symbols = {}

        def word_links(word):
            if word.named_entity and word.content:
                if word.content in words:
                    words[word.content].append(word.unique_id)
                else:
                    words[word.content] = [word.unique_id]

        def identifier_links(identifier):
            if identifier.content:
                if identifier.content in math_symbols:
                    math_symbols[identifier.content].append(identifier.unique_id)
                else:
                    math_symbols[identifier.content] = [identifier.unique_id]

        def formula_links(formula):
            math_env = formula.math_env
            if math_env:
                if math_env in math_symbols:
                    math_symbols[math_env].append(formula.unique_id)
                else:
                    math_symbols[math_env] = [formula.unique_id]

        for line in processed_lines_unique_ids:
            for token in line:
                if token.type == 'Word':
                    word_links(token)
                elif token.type == 'Identifier':
                    identifier_links(token)
                elif token.type == 'Formula':
                    formula_links(token)


        return words, math_symbols


    def handle_entire_formula(self, math_env):
        """
        Create a Formula object out of each delimiter (e.g. '$') of the math environment. The user can mouse click the
        delimiter to annotate the entire formula.
        :param math_env: String of the math environemnt (/formula).
        :return: 2 formula objects, one for each delimiter.
        """
        def create_formula(math_env):
            #math_env = math_env.replace('<math>', '')
            math_env = re.sub('<math.*?>', '', math_env)
            math_env = math_env.replace('</math>', '')
            #print('math_env: {}'.format(math_env))

            return Formula(
                str(uuid1()),
                type='Formula',
                highlight='#ffa500',
                content='$',
                endline=False,
                math_env=math_env
            )
        formula1, formula2 = create_formula(math_env), create_formula(math_env)
        return formula1, formula2


    def extract_words(self, line, line_num):
        """
        This method extracts the words that are contained in a line.
        If a named entity is contained, mark that.

        If keyword extraction is desired instead of NE tagging, this is where it should be changed

        :param line: a line in the file
        :param line_num: the number of the line in the file
        :return: List of the words fom the line (sentence) as Word() objects.
        """
        tagged_words = self.tagger.tag(line)
        return tagged_words

    def process_math_env(self, math_env, line_num):
        """
        This method extracts the identifiers that are contained in a math environment.
        :param math_env: the math_env that is being processed
        :param line_num: the number of line that the math environment is on
        :return: List of the Identifiers and other symbols in the math environment
        """

        #todo: for all math environemnt markers
        math_env = math_env.replace('$', '')

        #Select the class that should process (extract the identifiers and split) the math environment.
        #identifiers, split_math_env = FormulaSplitter(math_env).get_split_math_env()
        identifiers, split_math_env = CustomMathEnvParser(math_env).get_split_math_env()
        #self.__LOGGER__.debug(' process_math_env, split_math_env: {} '.format(split_math_env))

        #str_math_env = str(math_env).replace('<math>', '')
        str_math_env = re.sub('<math.*?>', '', str(math_env))
        str_math_env = str_math_env.replace('</math>', '')

        processed_maths_env = []
        for symbol in split_math_env:

            colour = '#c94f0c' if identifiers and symbol in identifiers else '#5c6670'
            endline = True if symbol == '\n' else False


            id_symbol = Identifier(
                str(uuid1()),
                type='Identifier',
                highlight=colour,
                content=symbol,
                endline=endline,
                math_env=str_math_env
            )

            self.identifier_line_dict[id_symbol.unique_id] = line_num

            processed_maths_env.append(id_symbol)

        # add the dollar signs back again
        formula1, formula2 = self.handle_entire_formula(str(math_env))
        processed_maths_env = [formula1] + processed_maths_env + [formula2]

        return processed_maths_env


    def add_unique_ids(self, processed_lines):
        """
        Generate unique_ids that allows reconstruction of the file at any later time (as long as file isn't modified.
        :param processed_lines_including_maths: All the lines contained in the document, processed.
        :return: The processed lines, with the custom generated unique_ids, a dicitonary of the lines, with the line
        number and a dictionary of the identifiers, with the lines they appear on (necessary for the creation of the
        word window.
        """

        def generate_id(line_num, token_num):
            """
            Generate a unique_id of the form [line number]---[token number].
            :param line_num: Number of line in the document.
            :param token_num: Number of token in the line.
            :return: Custom generated unique_id
            """
            unique_id = '{}---{}'.format(line_num, token_num)
            return unique_id

        line_dict = {}
        identifier_line_dict = {}
        for line_num, line in enumerate(processed_lines):
            line_dict[line_num] = []
            for token_num, token in enumerate(line):
                token.unique_id = generate_id(line_num, token_num)
                processed_lines[line_num][token_num] = token

                if token.type == 'Word' and token.named_entity:
                    line_dict[line_num].append(token)

                elif token.type == 'Identifier':
                    identifier_line_dict[token.unique_id] = line_num

                elif token.type == 'Formula':
                    identifier_line_dict[token.unique_id] = line_num

        return processed_lines, line_dict, identifier_line_dict



    def process(self):
        """
        This method is called from upload_file_view.py to process (parse) the file that the user selected.
        :return: A dictionary with the words and the line they appear on, a dictionary with the identifiers and what
                 line they appear on (needed for word window extraction) and a File object.
        """

        self.remove_math_envs()
        #necessary?
        lines = [p for p in self.file.split('\n')]
        word_lines = [self.extract_words(s, i) for i, s in enumerate(lines)]
        processed_lines = []
        for line_num, line in enumerate(word_lines):
            processed_line = []
            if len(line) < 1:
                processed_line.append(EmptyLine(uuid1()))
            for w in line:
                if re.search(r'__MATH_ENV__', w.content):
                    math_env = self.math_envs[0]
                    self.math_envs.pop(0)
                    processed_math_env = self.process_math_env(math_env, line_num)
                    processed_line += processed_math_env
                else:
                    processed_line.append(w)
            processed_lines.append(processed_line)

        processed_lines_unique_ids, line_dict, identifier_line_dict = self.add_unique_ids(processed_lines)
        linked_words, linked_math_symbols = self.form_links(processed_lines_unique_ids)
        #existing_annotations = self.read_annotation_file()
        existing_annotations = self.get_annotation_file_from_repo()
        file = File(processed_lines_unique_ids,
                               linked_words,
                               linked_math_symbols,
                               self.file_name,
                               existing_annotations)


        #print('*\n'*10)
        #print(file)
        #print('\n'*10)

        return (line_dict, identifier_line_dict, file)
