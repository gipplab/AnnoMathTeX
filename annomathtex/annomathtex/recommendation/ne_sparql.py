from ..recommendation.sparql import Sparql
from SPARQLWrapper import JSON
from ..recommendation.sparql_queries import named_entity_query
from ..config import recommendations_limit


class NESparql(Sparql):
    """
    get a string from one of the named entity recognizer and retrieve the corresponding Wikidata qid
    """


    def named_entity_search(self, search_string):
        """
        Doesn't use fuzzy search
        :param search_string:
        :return:
        """
        search_string_preprocessed = self.remove_special_characters(search_string)
        results_list = self.query(named_entity_query, search_string_preprocessed)
        print(results_list)
        return results_list

