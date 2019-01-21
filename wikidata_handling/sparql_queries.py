mathematical_expression_query = """
SELECT 
?item ?itemLabel 
WHERE {
  ?item wdt:P2534 ?mathematical_expression;
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

