from .sparql import Sparql
from SPARQLWrapper import JSON
from .sparql_queries import named_entity_query


class NESparql(Sparql):
    """
    get a string from one of the named entity recognizer and retrieve the corresponding Wikidata qid
    """


    def named_entity_search(self, search_string):
        """
        Doesn't use fuzzy search
        :param search_string:
        :return:
        """
        #use method from abstract base class
        entire_query = self.formulate_query(named_entity_query, search_string)

        self.sparql.setQuery(entire_query)
        self.sparql.setReturnFormat(JSON)
        query_results = self.sparql.query().convert()
        results = query_results['results']['bindings'][0]
        url = results['item']['value']
        qid = url.split('/')[-1]
        item_label = results['itemLabel']['value']
        item_description = results['itemDescription']['value']

        results_dict = {
            'qid': qid,
            'link': url,
            'item_label': item_label,
            'item_description': item_description
        }
        return results_dict
