from SPARQLWrapper import SPARQLWrapper
from abc import ABCMeta, abstractmethod
import re


class Sparql(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need to access wikidata query services
        - NESparql
        - MathSparql
    """

    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


    @classmethod
    def remove_special_characters(self, search_string):
        """
        Right now: only removing backslash.
        Also: don't search for strings like "1/2"
        :param search_string:
        :return:
        """
        search_string = search_string.replace('\\', '')
        return search_string


    @classmethod
    def remove_whitespaces(self, search_string):
        search_string = re.sub(r'\s', '', search_string)
        return search_string


    @classmethod
    def formulate_query(self, query, search_string):
        """

        :param query: tuple of query parts
        :param search_item: item that is being searched for, i.e. inserted into query
        :return: entire query
        """
        #entire_query = search_string.join(p for p in query)
        entire_query = "\'{}\'".format(search_string).join(p for p in query)
        return entire_query
