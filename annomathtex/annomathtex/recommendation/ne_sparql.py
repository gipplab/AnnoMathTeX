from ..recommendation.sparql import Sparql
from ..recommendation.sparql_queries import named_entity_query


class NESparql(Sparql):
    """
    This class handles all the non math environment related queries to Wikidata. These can be any words in the document
    but will for the most part be named entities extracted by the named entity tagger. In case the user wishes to
    annotate a word in the file that wasn't recognized by the named entity tagger, the process is still the same.
    This class inherits from the Sparql class, which contains most of the functionality necessary for accessing the
    Wikidata Query Service API.
    """


    def named_entity_search(self, search_string, limit=10):
        """
        This method uses the user selected word and queries the labels of wikidata items with that search strin.
        :param search_string: A string extracted by the named entitiy tagger.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """
        search_string_preprocessed = self.remove_special_characters(search_string)
        results_list = self.query(named_entity_query, search_string_preprocessed, limit)
        print(results_list)
        return results_list

