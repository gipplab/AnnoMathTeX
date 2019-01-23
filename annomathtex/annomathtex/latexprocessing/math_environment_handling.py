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
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


    def query(self, query_string, type='TeXString'):
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        query_results = self.sparql.query().convert()
        results = query_results['results']['bindings'][0]

        if type == 'defining_formula':
            return self.defining_formula(results)

        else:
            return self.tex_string(results)

    @classmethod
    def defining_formula(self, latex_formula):
        """
        Search for a formula with the defining formula property

        For mathML format of formula
        The defining formula property is written in MathML
        Currently only reutrns the MathML as string
        :param results:
        :return:
        """
        #todo: mathML to latex

        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        query_results = self.sparql.query().convert()
        results = query_results['results']['bindings'][0]


        _defining_formula = results['defining_formula']['value']
        return _defining_formula


    @classmethod
    def tex_string_contains(self, latex__part_formula):
        """
        Searching for items in wikidata that contain latex_part_formula

        tex_string_query is a tuple. Joining it on the latex formula gives the
        entire query with the tex formula at the right position.
        :param latex_formula:
        :return:
        """
        self.sparql.setQuery(tex_string_query.join(latex_part_formula))
        self.sparql.setReturnFormat(JSON)
        query_results = self.sparql.query().convert()
        results = query_results['results']['bindings'][0]
        tex_string = results['TeXString']['value']
        #should return description, qid, name of the item that was searched for
        return tex_string
































