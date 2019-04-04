

s = """
SELECT 
?item ?itemLabel ?itemDescription
WHERE{{  
  ?item ?label {} @en.  
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}    
}}
"""


p = s.format(4)

print(p)