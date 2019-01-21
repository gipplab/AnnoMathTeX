from SPARQLWrapper import SPARQLWrapper, JSON
from sparql_queries.mathematical_expression import mathematical_expression_query
import pandas as pd


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

sparql.setQuery(mathematical_expression_query)



sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.io.json.json_normalize(results['results']['bindings'])
print(results_df[['item.value', 'itemLabel.value']].head())


