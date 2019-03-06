from SPARQLWrapper import SPARQLWrapper, JSON
from .sparql_queries import tex_string_query, defining_formula_query, concat_query, formula_alias_query
from .sparql import Sparql



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

#import pywikibot

class WikidataQidPywikibot:
    """
    Useful properties:
        - P527: has part. E.g. mass-energy equivalence (E=mc^2, Q35875) has part energy (E, Q11379)
        - P361: part of. Inverse property of has part
        - P2534: defining formula. E.g. defining formula of mass-energy equivalence: E=mc^2
        - P1993: TeX string

    Claim object useful properties:
        - get_sources()
        - get_target()

    pywikibot.category - listify
    """
    pass


class MathSparql(Sparql):
    """
    import queries from separate file
    todo: remove redundancy
    todo: regex in query, to ignore whitespaces
    """
    #sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


    def aliases_search(self, search_string, limit=5):


        search_string_processed = self.remove_special_characters(search_string)
        search_string_processed = self.remove_whitespaces(search_string_processed)

        entire_query = self.formulate_query(
            formula_alias_query,
            search_string_processed
        )

        print('ENTIRE QUERY: ', entire_query)

        results = []
        try:
            self.sparql.setQuery(entire_query)
            self.sparql.setReturnFormat(JSON)
            query_results = self.sparql.query().convert()
            results = query_results['results']['bindings']  # [0]
            # results_cleaned = []
        except Exception as e:
            #print(e, 'Search string: ', search_string)
            print(e)

        results_dict = {}
        for i, r in enumerate(results):
            if i == limit: break
            item_description = None
            if 'itemDescription' in r:
                item_description = r['itemDescription']['value']
            url = r['item']['value']
            qid = url.split('/')[-1]
            item_label = r['itemLabel']['value']

            results_dict[i] = {
                'qid': qid,
                'link': url,
                'found_string': None,
                'item_label': item_label,
                'item_description': item_description
            }

            # results_cleaned.append(results_dict)
        # return results_cleaned
        return results_dict




    def defining_formula_contains(self, search_string):
        """
        Search for a formula with the defining formula property

        For mathML format of formula
        The defining formula property is written in MathML
        Currently only reutrns the MathML as string
        :param search_item:
        :return:
        """
        #(todo: mathML to latex) propably not really necessary
        #entire_query = self.formulate_query(defining_formula_query, search_item)

        search_string_without_space = self.remove_whitespaces(search_string)

        print('search_string_without_space', search_string_without_space)

        entire_query = self.formulate_query(
            concat_query,
            self.remove_special_characters(search_string_without_space)
        )

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
            #'defining_formula': defining_formula,
            'found_string': defining_formula,
            'item_label': item_label,
            'item_description': item_description
        }

        return results_dict


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


    def broad_search(self, search_string, limit=5):
        """
        Use concatenaed properties to query
        :param search_string: string from latex doc that is being search for
        :return:
        """

        entire_query = self.formulate_query(
                                            concat_query,
                                            self.remove_special_characters(search_string)
                                            )

        #print(search_string)

        results = []
        try:
            self.sparql.setQuery(entire_query)
            self.sparql.setReturnFormat(JSON)
            query_results = self.sparql.query().convert()
            results = query_results['results']['bindings']#[0]
            #results_cleaned = []
        except Exception as e:
            print(e, 'Search string: ', search_string)

        results_dict = {}
        for i, r in enumerate(results):
            if i == limit: break
            item_description = None
            if 'itemDescription' in r:
                item_description = r['itemDescription']['value']
            url = r['item']['value']
            qid = url.split('/')[-1]
            found_string = r['searchSpace']['value']
            item_label = r['itemLabel']['value']

            results_dict[i] = {
                'qid': qid,
                'link': url,
                'found_string': found_string,
                'item_label': item_label,
                'item_description': item_description
            }

            #results_cleaned.append(results_dict)
        #return results_cleaned
        return results_dict


    def formula_search(self, search_string, limit=5):

        search_string_without_space = self.remove_whitespaces(search_string)

        entire_query = self.formulate_query(
            concat_query,
            self.remove_special_characters(search_string_without_space)
        )

        pass




