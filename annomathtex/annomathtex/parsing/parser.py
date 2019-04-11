import re
import logging
from uuid import uuid1
from abc import ABCMeta, abstractmethod
from ..parsing.nehandling.named_entity_recognition import NLTK_NER
from ..models.identifier import Identifier
from ..models.formula import Formula
from ..models.empty_line import EmptyLine
from ..models.latexfile import LaTeXFile
from ..recommendation.arxiv_evaluation_handler import ArXivEvaluationListHandler
from ..recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from ..parsing.mathhandling.latexformlaidentifiers import FormulaSplitter
from ..parsing.mathhandling.custom_math_env_parser import CustomMathEnvParser


class Parser(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need to parse different input formats (tex, txt, html).
    """

    def __init__(self, request_file, file_name):
        """
        :param request_file: The file that the user selects to annotate.
        :param file_type: The type of the file (tex, txt, html).
        """
        logging.basicConfig(level=logging.INFO)
        self.__LOGGER__ = logging.getLogger(__name__)
        self.tagger = NLTK_NER()
        self.file = self.decode(request_file)
        self.file_name = file_name
        self.file_type = file_name.split('.')[-1]
        #self.__LOGGER__.debug(' FILE: {}'.format(self.file))
        self.math_envs = self.extract_math_envs()
        self.arXiv_evaluation_list_handler = ArXivEvaluationListHandler()
        self.wikipedia_evaluation_list_handler = WikipediaEvaluationListHandler()
        self.linked_words = {}
        self.linked_math_symbols = {}
        self.line_dict = {}
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

    @abstractmethod
    def remove_math_envs(self):
        """
        Remove all the math environments, process file without them and add them back later
        :return: File without math environments ('__MATH_ENV__' in place of each math_environment)
        """
        raise NotImplementedError('Function remove_math_envs() must be implemented')

    def remove_special_chars(self):
        """
        remove things like <href ....>
        #todo: implement
        :return:
        """
        pass

    def remove_math_envs(self):
        """
        Remove all the math environments, process file without them and add them back later
        :return: File without math environments ('__MATH_ENV__' in place of each math_environment)
        """
        for i, m in enumerate(self.math_envs):
            math_env = m
            self.__LOGGER__.debug(' in remove_math_envs() current math_env: {}'.format(m))
            try:
                #todo: only add space if necessary
                self.file = self.file.replace(math_env, ' __MATH_ENV__ ', 1)
            except Exception as e:
                self.__LOGGER__.error('math_env {} couldnt be replaced: {}'.format(math_env, e))
                continue

        #self.__LOGGER__.debug(' File after removing math_envs: {}'.format(self.file))


    def form_word_links(self, tagged_words):
        """
        Link identical words. This is used later when annotating a file, to only have to annotate a word once. All the
        other identical words in the file will be annotated automatically with the same field.
        #todo maybe: link also words that haven't been recognised as named entities.
        :param tagged_words: One line (sentence) of processed words.
        :return: None; The linked words are stored in the class dictionary linked_words
        """
        for word in tagged_words:
            if word.named_entity and word.content:
                if word.content in self.linked_words:
                    self.linked_words[word.content].append(word.unique_id)
                else:
                    self.linked_words[word.content] = [word.unique_id]

    def form_identifier_links(self, identifier):
        """
        Link identical identifiers. This is used later when annotating a file, to only have to annotate an
        identifier once. All the other identical identifiers in the file will be annotated automatically with the same
        field.
        :param identifier: The identifier that is being processed.
        :return: None; The linked identifier are stored in the class dictionary linked_math_symbols allong with the
                 linked formulae. They are stored together, to allow a math environment with only one identifier to be
                 treated the same way as an identifier within a math environemnt (e.g. $E$ is treated the same way as
                 'E' in $E=mc2$).
        """
        if identifier.content:
            if identifier.content in self.linked_math_symbols:
                self.linked_math_symbols[identifier.content].append(identifier.unique_id)
            else:
                self.linked_math_symbols[identifier.content] = [identifier.unique_id]

    def form_formula_links(self, formula1, formula2):
        """
        Link identical formulae. This is used later when annotating a file, to only have to annotate a
        formula once. All the other identical formulae in the file will be annotated automatically with the same
        field.
        :param formula1: The beginning delimiter of the formula (e.g. '$').
        :param formula2: The ending delimiter of the formula (e.g. '$').
        :return: None; The linked formulae are stored in the class dictionary linked_math_symbols allong with the
                 linked identifiers. They are stored together, to allow a math environment with only one identifier to
                 be treated the same way as an identifier within a math environemnt (e.g. $E$ is treated the same way
                 as 'E' in $E=mc2$).
        """
        math_env = formula1.math_env
        if math_env:
            if math_env in self.linked_math_symbols:
                self.linked_math_symbols[math_env] += [formula1.unique_id, formula2.unique_id]
            else:
                self.linked_math_symbols[math_env] = [formula1.unique_id, formula2.unique_id]

    def handle_entire_formula(self, math_env):
        """
        Create a Formula object out of each delimiter (e.g. '$') of the math environment. The user can mouse click the
        delimiter to annotate the entire formula.
        :param math_env: String of the math environemnt (/formula).
        :return: 2 formula objects, one for each delimiter.
        """

        # todo: put this in external class -> consistency   ??

        def create_formula():
            return Formula(
                str(uuid1()),
                type='Formula',
                highlight='#ffa500',
                content='$',
                endline=False,
                math_env=math_env
            )

        formula1, formula2 = create_formula(), create_formula()
        self.form_formula_links(formula1, formula2)

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
        self.form_word_links(tagged_words)
        self.line_dict[line_num] = [word for word in tagged_words if word.named_entity]
        return tagged_words

    def process_math_env(self, math_env, line_num):
        """
        This method extracts the identifiers that are contained in a math environment.
        :param math_env: the math_env that is being processed
        :param line_num: the number of line that the math environment is on
        :return: List of the Identifiers and other symbols in the math environment
        """

        # todo: for all math environemnt markers
        math_env = math_env.replace('$', '')

        #Select the class that should process (extract the identifiers and split) the math environment.
        #identifiers, split_math_env = FormulaSplitter(math_env).get_split_math_env()
        identifiers, split_math_env = CustomMathEnvParser(math_env).get_split_math_env()
        self.__LOGGER__.debug(' process_math_env, split_math_env: {} '.format(split_math_env))



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
            )

            self.identifier_line_dict[id_symbol.unique_id] = line_num

            processed_maths_env.append(id_symbol)
            self.form_identifier_links(id_symbol)

        # add the dollar signs back again
        formula1, formula2 = self.handle_entire_formula(str(math_env))
        processed_maths_env = [formula1] + processed_maths_env + [formula2]

        return processed_maths_env



    def process(self):
        """
        This method is called from upload_file_view.py to process (parse) the file that the user selected.
        :return: A dictionary with the words and the line they appear on, a dictionary with the identifiers and what
                 line they appear on (needed for word window extraction) and a File object.
        """

        self.remove_math_envs()
        #necessary?
        lines = [p for p in self.file.split('\n')]
        #self.__LOGGER__.debug(' Lines extracted: {}'.format(lines))
        processed_lines = [self.extract_words(s, i) for i, s in enumerate(lines)]
        #p_content = [word.content for line in processed_lines for word in line]
        #self.__LOGGER__.debug(' Lines processed: {}'.format(p_content))

        #todo: itertools
        processed_lines_including_maths = []
        for line_num, line in enumerate(processed_lines):
            processed_line = []
            if len(line) < 1:
                processed_line.append(EmptyLine(uuid1()))
            for w in line:
                if re.search(r'__MATH_ENV__', w.content):
                    #_, math_env = self.math_envs[0]
                    math_env = self.math_envs[0]
                    self.math_envs.pop(0)
                    processed_math_env = self.process_math_env(math_env, line_num)
                    processed_line += processed_math_env
                else:
                    processed_line.append(w)
            processed_lines_including_maths.append(processed_line)


        #todo
        #if self.file_type == 'txt':
        #    self.remove_tags()
        latex_file = LaTeXFile(processed_lines_including_maths, self.linked_words, self.linked_math_symbols, self.file_name)
        return (self.line_dict, self.identifier_line_dict, latex_file)
