"""
Project Mathematics:
    - https://www.wikidata.org/wiki/Wikidata:WikiProject_Mathematics
    - Contains information about properties that can be used to access mathematical content

Wikidata List of Properties:
    - https://www.wikidata.org/wiki/Wikidata:List_of_properties

Wikidata SPARQL examples
    - https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Finding_John_and_Sarah_Connor

Good tutorial
    - https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial


Steps:
    1. Get LaTeX math environment
    2. Split into components
        - Mathematical operators
        - Latex commands
        - identifiers
        - numbers
    3. Define sparql query that looks for the identifier
    4. Return ranking



Important:
    - mass: quantity symbol (P416): m



NOTE:
    this has to be in the clause, in order to get itemLabel and itemDescription
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
"""
################ MATH ####################

defining_formula_query ="""
    SELECT ?item ?itemLabel ?itemDescription ?definingFormula WHERE {{
      ?item wdt:P2534 ?definingFormula;
      FILTER( contains(?definingFormula, '{}'@en))
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {}
    """

tex_string_query ="""
    SELECT ?item ?itemLabel ?itemDescription ?teXString WHERE {{
         ?item wdt:P1993 ?teXString .
         FILTER( contains(?teXString, '{}'@en)) 
         SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}     
     }}
     LIMIT {}
     """


concat_query ="""
    SELECT ?item ?itemLabel ?itemDescription ?searchSpace WHERE {{
         ?item wdt:P1993|wdt:P2534 ?searchSpace;
         FILTER( contains(?searchSpace, '{}'@en)) 
         SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}     
     }}
     LIMIT {}
     """


formula_alias_query ="""
    SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE {{
        ?item skos:altLabel ?alias.
        FILTER(CONTAINS(?alias, '{}'@en))
        ?item wdt:P2534 ?dummy0 .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" .}}
    }}
    LIMIT {}
    """


identifier_query ="""
    SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE {{
        ?item wdt:P416 ?def.
        FILTER(CONTAINS(?def, '{}'@en))
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" .}}
    }}    
    LIMIT {}
    """

all_formulae_query = """{}
    SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE {{
        ?item skos:altLabel ?alias.
        ?item wdt:P2534 ?dummy0 .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" .}}
    }}
"""




################## Named Entities / Nouns ###################

#improve by making search fuzzy (contains) and fidning some way of limiting found instances
#to operators, symbols, science, ...

named_entity_query = """
    SELECT ?item ?itemLabel ?itemDescription WHERE{{  
      ?item ?label '{}'@en.  
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}    
    }}
    LIMIT {}
    """

concatenated_column_query = """
    SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE{{
      ?item ?label '{}'@en;
                    rdfs:label ?itemLabel;
      FILTER REGEX(?itemLabel, "[^0-9]").
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }} 
    }}
    LIMIT {}
    """
