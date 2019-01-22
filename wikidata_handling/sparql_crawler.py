from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from sparql_queries import mathematical_expression_query, emc, mass, emc_tex



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

        for k in definig_formula:
            print(k, definig_formula[k])
        #print(definig_formula)


    def defining_formula_pd(self, query_string):
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        results_df = pd.io.json.json_normalize(results['results']['bindings'])
        dfv = results_df[['defining_formula.value']]
        print(dfv)

    def tex_string(self, query_string):
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        results = results['results']['bindings'][0]
        tex_string = results['TeXString']['value']
        print(tex_string)






s = Sparql()
_query = emc_tex


s.tex_string(_query)
#s.defining_formula_json(_query)
#print(s.query(_query).head())


