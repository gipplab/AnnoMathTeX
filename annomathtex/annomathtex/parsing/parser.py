import re
import logging
import json
from uuid import uuid1
from abc import ABCMeta, abstractmethod
from ..parsing.nehandling.named_entity_recognition import NLTK_NER
from ..models.identifier import Identifier
from ..models.formula import Formula
from ..models.empty_line import EmptyLine
from ..models.latexfile import LaTeXFile
from ..recommendation.evaluation_list_handling import ArXivEvaluationListHandler, WikipediaEvaluationListHandler
from ..parsing.mathhandling.latexformlaidentifiers import FormulaSplitter
from ..config import recommendations_limit


class Parser(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need parse different input formats
    """

    def __init__(self, request_file):
        logging.basicConfig(level=logging.INFO)
        self.__LOGGER__ = logging.getLogger(__name__)
        self.tagger = NLTK_NER()
        self.file = self.decode(request_file)
        self.math_envs = self.extract_math_envs()
        self.arXiv_evaluation_list_handler = ArXivEvaluationListHandler()
        self.wikipedia_evaluation_list_handler = WikipediaEvaluationListHandler()
        self.linked_words = {}
        self.linked_math_symbols = {}
        self.line_dict = {}

    @abstractmethod
    def decode(self, request_file):
        raise NotImplementedError('Method decode must be implemented')

    @abstractmethod
    def extract_math_envs(self):
        raise NotImplementedError('must be impplemented')

    def remove_math_envs(self):
        """
        remove all the math environments
        process file without them and add them back later
        :return: file without math environments
        """
        for i, m in enumerate(self.math_envs):
            try:
                self.file = self.file.replace(m, '__MATH_ENV__', 1)
            except Exception as e:
                self.__LOGGER__.error('math_env {} couldnt be replaced: {}'.format(m, e))
                continue


    def form_word_links(self, tagged_words):
        for word in tagged_words:
            if word.named_entity and word.content:
                if word.content in self.linked_words:
                    self.linked_words[word.content].append(word.unique_id)
                else:
                    self.linked_words[word.content] = [word.unique_id]

    def form_symbol_links(self, symbol):
        if symbol.content:
            if symbol.content in self.linked_math_symbols:
                self.linked_math_symbols[symbol.content].append(symbol.unique_id)
            else:
                self.linked_math_symbols[symbol.content] = [symbol.unique_id]

    def form_formula_links(self, formula1, formula2):
        math_env = formula1.math_env
        if math_env:
            if math_env in self.linked_math_symbols:
                self.linked_math_symbols[math_env] += [formula1.unique_id, formula2.unique_id]
            else:
                self.linked_math_symbols[math_env] = [formula1.unique_id, formula2.unique_id]

    def get_word_window(self, line_num):
        word_window = []
        limit = int(recommendations_limit / 2)


        i = 0
        #todo: fix
        while i < limit:
            # lines before
            b = line_num - i
            # lines after
            a = line_num + i

            if b in self.line_dict:
                for word in reversed(self.line_dict[b]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['content'] == word.content, word_window)):
                        word_window.append({
                            'content': word.content,
                            'unique_id': word.unique_id
                        })
                        i += 1
            if a in self.line_dict:
                for word in reversed(self.line_dict[a]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['content'] in word.content, word_window)):
                        word_window.append({
                            'content': word.content,
                            'unique_id': word.unique_id
                        })
            i += 1

        if not word_window:
            word_window = [{}]

        return word_window[:10]

    def handle_entire_formula(self, math_env, line_num):

        # todo: put this in external class -> consistency   ??

        def create_formula():
            return Formula(
            str(uuid1()),
            type='Formula',
            highlight='yellow',
            content='$',
            endline=False,
            wikidata_result=None,
            word_window=json.dumps({'word_window': self.get_word_window(line_num)}),
            arXiv_evaluation_items=None,
            wikipedia_evaluation_items=None,
            math_env=math_env
        )

        formula1, formula2 = create_formula(), create_formula()
        self.form_formula_links(formula1, formula2)

        return formula1, formula2


    def extract_words(self, line, line_num):
        """
        This method extracts the words that are contained in a line.
        If a named entity is contained, mark that.
        :param line: a line in the file
        :param line_num: the number of the line in the file
        :return: List of the words fom sentence as Word() objects.
        """
        # if keyword extraction is desired instead of NE tagging, this is where it should be changed
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

        identifiers = FormulaSplitter(math_env).get_identifiers()

        try:
            split_regex = "|".join(str(i) for i in identifiers)
            split_regex = r"({})".format(split_regex)
            split_math_env = re.split(split_regex, math_env)
        except Exception as e:
            self.__LOGGER__.error('math_env {} couldnt be split: {}'.format(math_env, e))
            split_math_env = math_env

        processed_maths_env = []
        for symbol in split_math_env:

            if identifiers and symbol in identifiers:
                wikidata_result = None
                arXiv_evaluation_items = self.arXiv_evaluation_list_handler.check_identifiers(symbol)
                wikipedia_evaluation_items = self.wikipedia_evaluation_list_handler.check_identifiers(symbol)
            else:
                wikidata_result = None
                arXiv_evaluation_items = None
                wikipedia_evaluation_items = None

            endline = True if symbol == '\n' else False

            id_symbol = Identifier(
                str(uuid1()),
                type='Identifier',
                highlight='pink',
                content=symbol,
                endline=endline,
                wikidata_result=json.dumps({'w': wikidata_result}),
                word_window=json.dumps({'word_window': self.get_word_window(line_num)}),
                arXiv_evaluation_items=json.dumps({'arXiv_evaluation_items': arXiv_evaluation_items}),
                wikipedia_evaluation_items=json.dumps({'wikipedia_evaluation_items': wikipedia_evaluation_items})
            )

            processed_maths_env.append(id_symbol)
            self.form_symbol_links(id_symbol)

        # add the dollar signs back again
        formula1, formula2 = self.handle_entire_formula(str(math_env), line_num)
        processed_maths_env = [formula1] + processed_maths_env + [formula2]

        return processed_maths_env



    def process(self):

        self.__LOGGER__.debug(' process ')

        self.remove_math_envs()

        #necessary?
        lines = [p for p in self.file.split('\n')]

        processed_lines = [self.extract_words(s, i) for i, s in enumerate(lines)]

        #todo: itertools
        processed_lines_including_maths = []
        for line_num, line in enumerate(processed_lines):
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
            processed_lines_including_maths.append(processed_line)


        return LaTeXFile(processed_lines_including_maths, self.linked_words, self.linked_math_symbols)
