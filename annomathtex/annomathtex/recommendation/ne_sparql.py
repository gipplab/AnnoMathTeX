from ..recommendation.sparql import Sparql
from SPARQLWrapper import JSON
from ..recommendation.sparql_queries import named_entity_query
from ..config import recommendations_limit


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
        #entire_query = self.formulate_query(named_entity_query, search_string)

        entire_query = self.formulate_query(
                                            named_entity_query,
                                            self.remove_special_characters(search_string)
                                        )

        results = []
        try:
            self.sparql.setQuery(entire_query)
            self.sparql.setReturnFormat(JSON)
            query_results = self.sparql.query().convert()
            results = query_results['results']['bindings']#[0]
        except Exception as e:
            print(e, 'Search string: ', search_string)

        results_dict = {}
        for i, r in enumerate(results):
            if i == recommendations_limit: break
            item_description = None
            if 'itemDescription' in r:
                item_description = r['itemDescription']['value']
            url = r['item']['value']
            qid = url.split('/')[-1]
            found_string = None
            item_label = r['itemLabel']['value']

            results_dict[i] = {
                'qid': qid,
                'link': url,
                'found_string': found_string,
                'item_label': item_label,
                'item_description': item_description
            }
        return results_dict

