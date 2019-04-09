from .sparql_queries import *
from ..recommendation.sparql import Sparql


class MathSparql(Sparql):
    """

    """

    def aliases_search(self, search_string):
        """

        :param search_string:
        :return:
        """
        search_string_processed = self.remove_special_characters(search_string)
        search_string_processed = self.remove_whitespaces(search_string_processed)
        results_list = self.query(formula_alias_query, search_string_processed)

        return results_list




    def defining_formula_search(self, search_string):
        """
        Search for a formula with the defining formula property

        For mathML format of formula
        The defining formula property is written in MathML
        Currently only reutrns the MathML as string
        :param search_item:
        :return:
        """
        search_string_without_space = self.remove_whitespaces(search_string)
        search_string_preprocessed = self.remove_special_characters(search_string_without_space)

        results_list = self.query(defining_formula_query, search_string_preprocessed)

        return results_list


    def tex_string_contains(self, search_string):
        """
        Searching for items in wikidata that contain latex_part_formula

        tex_string_query is a tuple. Joining it on the latex formula gives the
        entire query with the tex formula at the right position.
        :param latex_formula:
        :return:
        """
        results_list = self.query(tex_string_query, search_string)
        return results_list


    def concat_search(self, search_string):
        """
        Use concatenaed properties to query
        :param search_string: string from latex doc that is being search for
        :return:
        """
        search_string_preprocessed = self.remove_special_characters(search_string)
        results_list = self.query(concat_query, search_string_preprocessed)
        return results_list


    def identifier_search(self, search_string):
        """
        Mainly used module
        :param identifier_string: string of the identifier that is queried
        :return:
        """

        results_list = self.query(identifier_query, search_string)
        print('RESULTS DICT: \n\n\n\n')
        print(results_list)
        print('\n'*4)
        return results_list




