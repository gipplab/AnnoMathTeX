from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

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
    https://people.wikimedia.org/~bearloga/notes/wdqs-python.html
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
    def defining_formula(self, results):
        #TODO add rest
        _defining_formula = results['defining_formula']
        return _defining_formula


    @classmethod
    def tex_string(self, results):
        tex_string = results['TeXString']['value']
        return tex_string

