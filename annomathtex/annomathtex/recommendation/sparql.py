from SPARQLWrapper import SPARQLWrapper, JSON
from abc import ABCMeta, abstractmethod
from ..config import recommendations_limit
import re
import logging


class Sparql(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need to access wikidata query services
        - NESparql
        - MathSparql
    """

    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        logging.basicConfig(level=logging.INFO)
        self.__LOGGER__ = logging.getLogger(__name__)

    def remove_special_characters(self, search_string):
        """
        Right now: only removing backslash.
        Also: don't search for strings like "1/2"
        :param search_string:
        :return:
        """
        search_string = search_string.replace('\\', '')
        return search_string

    def remove_whitespaces(self, search_string):
        search_string = re.sub(r'\s', '', search_string)
        return search_string

    def formulate_query(self, query_string, search_string, limit=recommendations_limit):
        """

        :param query: tuple of query parts
        :param search_item: item that is being searched for, i.e. inserted into query
        :return: entire query
        """

        #for other formats of query strings:
        #entire_query = search_string.join(p for p in query)
        #entire_query = "\'{}\'".format(search_string).join(p for p in query)

        entire_query = query_string.format(search_string, limit)
        return entire_query


    def query(self, query_string, search_string, limit=recommendations_limit):
        """

        :param query_string:
        :param search_string:
        :param limit:
        :return:
        """

        entire_query = query_string.format(search_string, limit)
        results = []
        try:
            self.sparql.setQuery(entire_query)
            self.sparql.setReturnFormat(JSON)
            query_results = self.sparql.query().convert()
            results = query_results['results']['bindings']
        except Exception as e:
            self.__LOGGER__.error(e)

        """results_dict = {}
        for i, r in enumerate(results):
            if i == recommendations_limit: break
            item_description = None
            if 'itemDescription' in r:
                item_description = r['itemDescription']['value']
            url = r['item']['value']
            qid = url.split('/')[-1]
            item_label = r['itemLabel']['value']

            #Depending on the query string, other fields which aren't used at the moment may be available.
            results_dict[i] = {
                'qid': qid,
                'link': url,
                'item_label': item_label,
                'item_description': item_description
            }

        return results_dict"""

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
