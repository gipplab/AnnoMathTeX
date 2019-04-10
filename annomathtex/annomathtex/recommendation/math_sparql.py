from .sparql_queries import *
from ..recommendation.sparql import Sparql


class MathSparql(Sparql):
    """
    This class handles all math environment related queries to Wikidata. It inherits from the Sparql class, which
    contains most of the functionality necessary for accessing the Wikidata Query Service API.
    """

    def aliases_search(self, search_string):
        """
        This method queries the aliases (the also known as property) of a wikidata item.
        :param search_string: The string that is being queried for.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """
        search_string_processed = self.remove_special_characters(search_string)
        search_string_processed = self.remove_whitespaces(search_string_processed)
        results_list = self.query(formula_alias_query, search_string_processed)

        return results_list


    def defining_formula_search(self, search_string):
        """
        This method queries for a formula using the defining formula property.
        The defining formula property is written in MathML.
        Currently only reutrns the MathML as string.
        :param search_string: The string that is being queried for.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """
        search_string_without_space = self.remove_whitespaces(search_string)
        search_string_preprocessed = self.remove_special_characters(search_string_without_space)

        results_list = self.query(defining_formula_query, search_string_preprocessed)

        return results_list


    def tex_string_contains(self, search_string):
        """
        This method queries for items in wikidata that contain the search string in the property "latex formula".
        :param search_string: The string that is being queried for.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """
        results_list = self.query(tex_string_query, search_string)
        return results_list


    def concat_search(self, search_string):
        """
        This method uses concatenaed properties for the query.
        :param search_string: The string that is being queried for.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """
        search_string_preprocessed = self.remove_special_characters(search_string)
        results_list = self.query(concat_query, search_string_preprocessed)
        return results_list


    def identifier_search(self, search_string):
        """
        Method used at the moment when the user mouse clicks an identifiers.
        This method searches for the identifiers in the "has par" property of wikidata items.
        :param search_string: The string that is being queried for.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """

        results_list = self.query(identifier_query, search_string)
        return results_list




