#from annomathtex.annomathtex.recommendation.math_sparql import MathSparql


#f = MathSparql().all_formulae_search()

#print(f)

from SPARQLWrapper import SPARQLWrapper, JSON
import re
import os
import json



formula_query = """
SELECT ?item ?itemLabel ?formula ?itemDescription ?identifier ?identifierLabel ?identifierDescription WHERE {
  ?item wdt:P2534 ?formula.
  #OPTIONAL{?identifier wdt:416 ?symbol .}
  OPTIONAL{?item wdt:P527 ?identifier .} 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""

identifier_query = """
SELECT ?item ?itemLabel ?itemDescription ?identifier WHERE {
  ?item wdt:P416 ?identifier.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
#LIMIT 3
"""

class Sparql(object):

    def __init__(self):
        # Used to access the wikidata query service API
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.q = formula_query


    def query(self, q):
        try:
            self.sparql.setQuery(q)
            self.sparql.setReturnFormat(JSON)
            query_results = self.sparql.query().convert()
            results = query_results['results']['bindings']
        except Exception as e:
            print(e)
            results = []

        return results


    def process_identifiers(self):
        results = self.query(identifier_query)
        identifier_dict = {}
        for i in results:
            #print(i)
            qid = i['item']['value']
            try:
                qid = re.findall(r'[Q|P][0-9]+$', qid)[0]
            except Exception as e:
                print(e)
                print(i)
            name = i['itemLabel']['value']
            string = i['identifier']['value']
            identifier_dict[qid] = {'name': name, 'string': string}
        return identifier_dict

    def process_formulae(self):
        """
        This method executes all the queries that may be sent to the wikidata query service API. The results are
        cleaned and returned as a list of dictionaries.
        :param query_string: The query that is being used.
        :param search_string: The string that is being searched for through the wikidata query service API.
        :param limit: The limit for the number of results.
        :return: A list of dictionaries, where each dictionary is one result from the search.
        """
        formulae = self.query(formula_query)
        identifiers = self.process_identifiers()

        formula_concepts = {}
        for i, r in enumerate(formulae):
            if 'itemDescription' in r:
                item_description = r['itemDescription']['value']
            url = r['item']['value']
            qid = url.split('/')[-1]
            item_label = r['itemLabel']['value']


            formula = r['formula']
            mathML = formula['value']
            try:
                tex = re.findall(r'(?<=alttext=\"{\\displaystyle ).*?(?=}\">)', mathML)[0]
            except:
                tex = ''


            identifier = None

            if 'identifier' in r:
                identifier_value = r['identifier']['value']
                identifier_qid = re.findall(r'[Q|P][0-9]+$', identifier_value)[0]
                try:
                    identifier = identifiers[identifier_qid]
                except KeyError as _:
                    continue



            if item_label not in formula_concepts:
                if identifier:
                    identifiers_dict = {'names': [identifier['name']], 'strings': [identifier['string']]}
                else:
                    identifiers_dict = {'names': [], 'strings': []}
                formula_concepts[item_label] = {
                    'qid': qid,
                    'formula': tex,
                    #'identifiers': [identifier] if identifier else []
                    'identifiers': identifiers_dict
                }
            else:
                if identifier:
                    try:
                        existing_identifiers = formula_concepts[item_label]['identifiers']
                        if identifier['name'] not in existing_identifiers['names']:
                            existing_identifiers['names'].append(identifier['name'])
                        if identifier['string'] not in existing_identifiers['strings']:
                            existing_identifiers['strings'].append(identifier['string'])

                    except Exception as e:
                        print(e)


        return formula_concepts






s = Sparql()
f = s.process_formulae()

path = os.path.join(os.getcwd(), 'annomathtex', 'annomathtex', 'recommendation', 'evaluation_files', 'wikidata_formulae.json')
with open(path, 'w') as outfile:
    json.dump(f, outfile)