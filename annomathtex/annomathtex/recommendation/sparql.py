from SPARQLWrapper import SPARQLWrapper, JSON
from abc import ABCMeta
from ..config import recommendations_limit
import re
import logging


logging.basicConfig(level=logging.INFO)
sparql_logger = logging.getLogger(__name__)


class Sparql(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need to access wikidata query services
        - NESparql
        - MathSparql
    """

    def __init__(self):
        # Used to access the wikidata query service API
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    def remove_special_characters(self, search_string):
        """
        Right now: only removing backslash.
        :param search_string:
        :return:
        """
        search_string = search_string.replace('\\', '')
        return search_string

    def remove_whitespaces(self, search_string):
        """
        Removes all whitespaces from the search string. This improves the results in many cases.
        :param search_string: The string that is being searched for through the wikidata query service API.
        :return: Processed search string.
        """

        search_string = re.sub(r'\s', '', search_string)
        return search_string


    def query(self, query_string, search_string, limit=recommendations_limit):
        """
        This method executes all the queries that may be sent to the wikidata query service API. The results are
        cleaned and returned as a list of dictionaries.
        :param query_string: The query that is being used.
        :param search_string: The string that is being searched for through the wikidata query service API.
        :param limit: The limit for the number of results.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """
        entire_query = query_string.format(search_string, limit)
        results = []

        try:
            self.sparql.setQuery(entire_query)
            self.sparql.setReturnFormat(JSON)
            query_results = self.sparql.query().convert()
            results = query_results['results']['bindings']
        except Exception as e:
            sparql_logger.error(e)

        results_list = []
        for i, r in enumerate(results):
            if i == recommendations_limit: break
            item_description = None
            if 'itemDescription' in r:
                item_description = r['itemDescription']['value']
            url = r['item']['value']
            qid = url.split('/')[-1]
            item_label = r['itemLabel']['value']

            results_list.append({
                'qid': qid,
                'link': url,
                'name': item_label,
                'item_description': item_description
            })

        return results_list
