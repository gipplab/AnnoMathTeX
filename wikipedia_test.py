import requests
from bs4 import BeautifulSoup
import wikipedia


print(wikipedia.search("quantum harmonic oscillator", results=5))

"""url = "https://en.wikipedia.org/w/index.php?title=Quantum_harmonic_oscillator&action=edit"


r = requests.get(url)
content = r.content.decode('utf-8')

soup = BeautifulSoup(content)

divs = soup.find_all("textarea")

wikiPreview = "wikiPreview"

text = soup.find("textarea").contents[0]
print(text)"""


#for d in divs:
#    #if d.get("id") == wikiPreview:
#    print(d.contents[0])
