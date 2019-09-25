import json
import logging
from django.http import HttpResponse

from ...recommendation.arxiv_evaluation_handler import ArXivEvaluationListHandler
from ...recommendation.wikipedia_evaluation_handler import WikipediaEvaluationListHandler
from ...recommendation.static_wikidata_handler import StaticWikidataHandler
from ...recommendation.manual_recommendations_handler import ManualRecommendationsHandler
from ...recommendation.formula_concept_db_handler import FormulaConceptDBHandler
from ...views.helper_classes.data_repo_handler import DataRepoHandler
from ...views.helper_classes.cache_handler import CacheHandler
from ...config import *

logging.basicConfig(level=logging.INFO)
token_clicked_handler_logger = logging.getLogger(__name__)

class TokenClickedHandler:
    #todo: better naming (queryDict, etc.)

    """
    This class handles the use case, when the user selects a token (word, identifier or formula) to annotate.
    Depending on the type of the token, different types of data are sent back to the frontend.

    Identifier:
        - Wikidata query is made
        - ArXiv evaluation list is checked for matches8
        - Wikipedia evaluation list is checked for matches
        - Word window is computed

    Formula:
        - Wikidata query is made
        - Word window is computed

    Word (must not necessarily be named entity, as found by tagger):
        - Wikidata query is made


    For identifier and formulae, additionaly the concatenated results are computed, taking results from each of the
    sources and combining them in one column.

    :param request: Request object. Request made by the user through the frontend.
    :return: The rendered response containing the template name, the necessary form and the response data.
    """

    def __init__(self, request, items):
        self.items = items
        self.arXiv_evaluation_items, \
        self.wikipedia_evaluation_items, \
        self.wikidata1_results, \
        self.wikidata2_results, \
        self.word_window, \
        self.formula_concept_db, \
        self.manual_recommendations = [], [], [], [], [], [], []


    def get_recommendations(self):
        #todo: simplify
        token_type_dict = self.items['tokenType']
        token_type = [k for k in token_type_dict][0]
        unique_id = [k for k in self.items['uniqueId']][0]

        token_clicked_handler_logger.info('Type: {}'.format(token_type))

        if token_type == 'Identifier':
            self.handle_identifier()

        elif token_type == 'Formula':
            self.handle_formula()

        self.word_window = self.get_word_window(unique_id)

        return HttpResponse(
            json.dumps({'arXivEvaluationItems': self.fill_to_limit(self.arXiv_evaluation_items),
                        'wikipediaEvaluationItems': self.fill_to_limit(self.wikipedia_evaluation_items),
                        'wikidata1Results': self.fill_to_limit(self.wikidata1_results),
                        'wikidata2Results': self.fill_to_limit(self.wikidata2_results),
                        'wordWindow': self.fill_to_limit(self.word_window),
                        'formulaConceptDB': self.fill_to_limit(self.formula_concept_db),
                        'manual': self.fill_to_limit(self.manual_recommendations)}),
                        content_type='application/json'
        )


    def handle_identifier(self):
        search_string = [k for k in self.items['queryDict']][0]
        unique_id = [k for k in self.items['uniqueId']][0]
        #is this bad form?
        self.wikidata1_results = StaticWikidataHandler().check_identifiers(search_string)
        self.arXiv_evaluation_items = ArXivEvaluationListHandler().check_identifiers(search_string)
        self.wikipedia_evaluation_items = WikipediaEvaluationListHandler().check_identifiers(search_string)
        manual_recommendations = DataRepoHandler().get_manual_recommendations()
        self.manual_recommendations = ManualRecommendationsHandler(manual_recommendations).check_identifier_or_formula(
            search_string)

        return

    def handle_formula(self):
        math_env = self.items['mathEnv']['dummy']
        annotations = self.items['annotations']
        #todo: remove redundancy
        unique_id = [k for k in self.items['uniqueId']][0]
        self.wikidata1_results, self.wikidata2_results = StaticWikidataHandler().check_formulae(math_env, annotations)
        self.formula_concept_db = FormulaConceptDBHandler().query_tex_string(math_env)
        manual_recommendations = DataRepoHandler().get_manual_recommendations()
        self.manual_recommendations = ManualRecommendationsHandler(manual_recommendations).check_identifier_or_formula(
            math_env)

        return

    def fill_to_limit(self, dict_list):
        recommendations_limit = 10
        dict_list += [{'name': ''} for _ in range(recommendations_limit - len(dict_list))]
        return dict_list


    def get_word_window(self, unique_id):
        """
        This method produces the word window for a selected (by the user) formula or identifier. It iteratively takes
        named entities from the lines before and after the selected token(s) to fill the number of named entities as
        specified by the recommendation limit.
        :param unique_id: The unique id if the token (identifier or formula).
        :return: a list of named entities that appear around the selected token.
        """

        word_window = []
        limit = int(recommendations_limit / 2)
        #dicts = self.cache_to_dicts()
        dicts = CacheHandler().cache_to_dicts()
        identifier_line_dict = dicts['identifiers']
        line_dict = dicts['lines']
        if unique_id in identifier_line_dict:
            line_num = identifier_line_dict[unique_id]
        else:
            return []

        i = 0
        while i < limit:
            # lines before
            b = line_num - i
            # lines after
            a = line_num + i

            if b in line_dict:
                for word in reversed(line_dict[b]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['name'] == word.content.lower(), word_window)):
                        word_window.append({
                            'name': word.content.lower(),
                            #'unique_id': word.unique_id
                        })
                        i += 1
            if a in line_dict:
                for word in reversed(line_dict[a]):
                    # value not yet in word window
                    if not list(filter(lambda d: d['name'] in word.content.lower(), word_window)):
                        word_window.append({
                            'name': word.content.lower(),
                            #'unique_id': word.unique_id
                        })
            i += 1
        if not word_window:
            word_window = [{}]
        return word_window[:recommendations_limit]


