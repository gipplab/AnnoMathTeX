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

    def __init__(self, items):
        self.items = items


    def get_recommendations(self):



        recommendations_dict = {'arXivEvaluationItems': [],
                        'wikipediaEvaluationItems': [],
                        'wikidata1Results': [],
                        'wikidata2Results': [],
                        'wordWindow': [],
                        'formulaConceptDB': [],
                        'manual': []}


        search_string = [k for k in self.items['searchString']][0]
        token_type_dict = self.items['tokenType']
        token_type = [k for k in token_type_dict][0]
        unique_id = [k for k in self.items['uniqueId']][0]
        math_env = self.items['mathEnv']['dummy']
        annotations = self.items['annotations']

        token_clicked_handler_logger.info('Type: {}'.format(token_type))

        all_manual_recommendations = DataRepoHandler().get_manual_recommendations()

        if token_type == 'Identifier':
            recommendations_dict['arXivEvaluationItems'] = ArXivEvaluationListHandler().check_identifiers(search_string)
            recommendations_dict['wikipediaEvaluationItems'] = WikipediaEvaluationListHandler().check_identifiers(search_string)
            recommendations_dict['wikidata1Results'] = StaticWikidataHandler().check_identifiers(search_string)

        elif token_type == 'Formula':
            recommendations_dict['wikidata1Results'], recommendations_dict['wikidata2Results'] = StaticWikidataHandler().check_formulae(math_env, annotations)
            recommendations_dict['formulaConceptDB'] = FormulaConceptDBHandler().query_tex_string(math_env)
            #token_clicked_handler_logger.info(recommendations_dict['formulaConceptDB'])

        else:
            token_clicked_handler_logger.info('Faulty token_type: {}'.format(token_type))





        recommendations_dict['wordWindow'] = self.get_word_window(unique_id)

        recommendations_dict['manual'] = ManualRecommendationsHandler(
                                                all_manual_recommendations).check_identifier_or_formula(search_string)

        data_repo_handler = DataRepoHandler()
        all_wikidata_identifiers = data_repo_handler.get_wikidata_identifiers_by_name()
        all_wikidata_formulae = data_repo_handler.get_wikidata_formulae()
        all_math_items = data_repo_handler.get_math_wikidata_items()

        token_clicked_handler_logger.info(type(all_math_items))
        token_clicked_handler_logger.info(all_math_items["metabiaugmented hexagonal prism"])


        def pp(dict_list, source):
            """
            post process: add QID and fill to recommendations limit
            :param dict_list: ditionary list of recommendations from one source
            :return:
            """
            def add_qid_identifier(r):
                """
                :param r: single recommendation
                :return:
                """
                name = r['name']
                if name in all_wikidata_identifiers:
                    r['qid'] = all_wikidata_identifiers[name]['qid']
                else:
                    r['qid'] = 'N/A'
                #token_clicked_handler_logger.info(r)
                return r

            def add_qid_formula(r):
                """
                :param r: single recommendation
                :return:
                """
                name = r['name']
                if name in all_wikidata_formulae:
                    r['qid'] = all_wikidata_formulae[name]['qid']
                else:
                    r['qid'] = 'N/A'
                return r

            def add_qid_all_math(r):



                if source not in ['wikidata1Results', 'wikidata2Results']:

                    name = r['name']
                    if name in all_math_items:
                        r['qid'] = all_math_items[name]
                    else:
                        r['qid'] = 'N/A'
                r['name'] = r['name'].replace("\'", '__APOSTROPH__')
                return r


            dict_list = list(map(add_qid_all_math, dict_list))


            dict_list += [{'name': ''} for _ in range(recommendations_limit - len(dict_list))]
            return dict_list

        recommendations_dict_pp = dict(map(lambda kv: (kv[0], pp(kv[1], kv[0])), recommendations_dict.items()))
        response = HttpResponse(json.dumps(recommendations_dict_pp), content_type='application/json')
        return response, recommendations_dict_pp

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


