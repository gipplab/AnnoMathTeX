from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from sparql_queries import mathematical_expression_query



class Sparql:
    """
    https://people.wikimedia.org/~bearloga/notes/wdqs-python.html
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


    def query(self, query_string):
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        results_df = pd.io.json.json_normalize(results['results']['bindings'])
        return results_df[['item.value', 'itemLabel.value']]#.head()





s = Sparql()

_query = mathematical_expression_query


print(s.query(_query).head())



