import bz2
import codecs
import re
import time
import json

file = '/volumes/Stuff/latest-all.json.bz2'
out_path = '/volumes/Stuff/unzipped/test.json'
source_file = bz2.BZ2File(file, "r")
output_file = codecs.open(out_path,'w+','utf-8')

all_items = {}
start = time.time()
count = 0
for line in source_file:
    line_decoded = line.decode('utf-8')
    qid_search = re.search(r'(?<=\"id\":\")Q[0-9]+', line_decoded)
    name_search = re.search(r'(?<=\"language\":\"en\",\"value\":\").*?(?=\")', line_decoded, re.IGNORECASE)

    if qid_search:
        qid = qid_search.group()#[0]

    if name_search:
        name = name_search.group()

    count += 1
    if count == 100000:
        break

    if qid_search and name_search:
        #output_file.write(json.dumps({name:qid}))
        all_items[name]=qid


end = time.time() - start
print('time: {}'.format(end))
print('items: {}'.format(len(list(all_items.keys()))))
with open(out_path, 'w') as o:
    json.dump(all_items, o)

