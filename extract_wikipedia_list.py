import urllib.request
import html2text
import re
from operator import itemgetter
import json


fp = urllib.request.urlopen("https://en.wikipedia.org/wiki/User:Physikerwelt")
filebytes = fp.read()

filestr = filebytes.decode("utf8")
fp.close()

h = html2text.HTML2Text()
h.ignore_links = True

prettified = h.handle(filestr)

#mystr_split = prettified.split('**Definitions:**')
lines = prettified.splitlines()

identifier_dict = {}

i = 0
for s in lines:
    if '{\\displaystyle' in s:
        i += 1
        #print(s)
        identifier = re.search(r'(?<= \* ).*?(?= \{)', s).group()
        displaystyle = re.search(r'(?<= \{\\displaystyle ).*?(?= ?\} !)', s).group()
        wikimedia_link = re.search(r'https:.*?(?=\))', s).group()
        description = re.search(r'(?<=: ).*?(?= \()', s).group()
        value = s.split()[-1][1:-1]

        if len(identifier) < 5:
            if displaystyle in identifier_dict:
                #identifier_dict[displaystyle].append((value, identifier, description, wikimedia_link))
                identifier_dict[displaystyle].append({
                    'value': value,
                    'identifier': identifier,
                    'description': description,
                    'wikimedia_link': wikimedia_link
                })
            else:
                #identifier_dict[displaystyle] = [(value, identifier, description, wikimedia_link)]
                identifier_dict[displaystyle] = [{
                    'value': value,
                    'identifier': identifier,
                    'description': description,
                    'wikimedia_link': wikimedia_link
                }]


for k in identifier_dict:
    identifier_dict[k].sort(key=itemgetter('value'), reverse=True)


#for k in identifier_dict:
#    print(k, identifier_dict[k])




#with open('wikipedia_list.json', 'w') as outfile:
#    json.dump(identifier_dict, outfile)


with open('wikipedia_list.json', 'r') as infile:
    i = json.load(infile)

#for k in i:
#    print(k, i[k])




