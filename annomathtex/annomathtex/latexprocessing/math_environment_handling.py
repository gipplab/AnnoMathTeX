from SPARQLWrapper import SPARQLWrapper, JSON
from .sparql_queries import tex_string_query, defining_formula_query

"""
Math environment handling involves the revognition of formulae and identifiers.
These have to be recognised as being individual parts.
Then values from the surrounding text (NLP) should be associated with them,
and/or the corresponding wikidata Qid added.

Wikidata Qid can be extracted using
    - pywikibot
    - sparql

Steps:
    - extract math environment
    - extract identifiers
    - extract formulae
        -should add some kind of fuzzy string matching
    - access wikidata
    - find Qid

Ideas:
    - Crawl wikidata, extracting all physical quanities
    
"""

import pywikibot

class WikidataQidPywikibot:
    """
    Useful properties:
        - P527: has part. E.g. mass-energy equivalence (E=mc^2, Q35875) has part energy (E, Q11379)
        - P361: part of. Inverse property of has part
        - P2534: defining formula. E.g. defining formula of mass-energy equivalence: E=mc^2
        - P1993: TeX string

    Claim object useful properties:
        - get_sources()
        -get_target()

    pywikibot.category - listify
    """


class Sparql:
    """
    import queries from separate file
    todo: remove redundancy
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


    def formulate_query(self, query, search_item):
        """

        :param query: tuple of query parts
        :param search_item: item that is being searched for, i.e. inserted into query
        :return: entire query
        """

        entire_query = search_item.join(p for p in query)
        return entire_query

    @classmethod
    def defining_formula_contains(self, search_item):
        """
        Search for a formula with the defining formula property

        For mathML format of formula
        The defining formula property is written in MathML
        Currently only reutrns the MathML as string
        :param search_item:
        :return:
        """
        #todo: mathML to latex
        entire_query = self.formulate_query(defining_formula_query, search_item)

        self.sparql.setQuery(entire_query)
        self.sparql.setReturnFormat(JSON)
        query_results = self.sparql.query().convert()
        results = query_results['results']['bindings'][0]
        url = results['item']['value']
        qid = url.split('/')[-1]
        defining_formula = results['definingFormula']['value']
        item_label = results['itemLabel']['value']
        item_description = results['itemDescription']['value']

        results_dict = {
            'qid': qid,
            'link': url,
            'defining_formula': defining_formula,
            'item_label': item_label,
            'item_description': item_description
        }

        return results_dict


    @classmethod
    def tex_string_contains(self, search_item):
        """
        Searching for items in wikidata that contain latex_part_formula

        tex_string_query is a tuple. Joining it on the latex formula gives the
        entire query with the tex formula at the right position.
        :param latex_formula:
        :return:
        """
        entire_query = self.formulate_query(tex_string_query, search_item)

        self.sparql.setQuery(entire_query)
        self.sparql.setReturnFormat(JSON)
        query_results = self.sparql.query().convert()
        results = query_results['results']['bindings'][0]
        url = results['item']['value']
        qid = url.split('/')[-1]
        tex_string = results['teXString']['value']
        item_label = results['itemLabel']['value']
        item_description = results['itemDescription']['value']

        results_dict = {
            'qid': qid,
            'link': url,
            'tex_string': tex_string,
            'item_label': item_label,
            'item_description': item_description
        }
        return results_dict
































