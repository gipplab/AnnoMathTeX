from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from sparql_queries import mathematical_expression_query, emc, mass



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
        #return results_df[['item.value', 'defining_formula.value']]  # .head()


    def defining_formula_json(self, query_string):
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        definig_formula = results['results']['bindings'][0]['defining_formula']
        print(definig_formula)


    def defining_formula_pd(self, query_string):
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_df = pd.io.json.json_normalize(results['results']['bindings'])
        dfv = results_df[['defining_formula.value']]
        print(dfv)





#s = Sparql()

_query = emc
#print(s.query(_query).head())


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


results_df = pd.io.json.json_normalize(results['results']['bindings'])
print(list(results_df.columns))

dfv = results_df[['defining_formula.value']]
print(dfv)

#definig_formula = results['results']['bindings'][0]['defining_formula']
#print(definig_formula)

#for k in results:
#    print(k, results[k])

