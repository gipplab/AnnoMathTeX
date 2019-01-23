from SPARQLWrapper import SPARQLWrapper
from abc import ABCMeta, abstractmethod


class Sparql(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need to access wikidata query services
        - NESparql
        - MathSparql
    """

    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


    @classmethod
    def formulate_query(self, query, search_string):
        """

        :param query: tuple of query parts
        :param search_item: item that is being searched for, i.e. inserted into query
        :return: entire query
        """
        entire_query = search_string.join(p for p in query)
        return entire_query
