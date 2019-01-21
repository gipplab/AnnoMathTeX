from multiprocessing import Process, Queue, Pool
from wikidata.client import Client
import random
from time import time
import string
import os



"""output = Queue()

def iterate_wikidata_pages(m, output):
    start, end, process_no = m

    process = 'Process number: ' + str(process_no)
    client = Client()
    for qid in range(start, end):
        try:
            if qid % 10 == 0:
                print(process, ': ', qid)
            entity = client.get('Q' + str(qid), load=True)
            if 'claims' in entity.attributes:
                claims = entity.attributes['claims']
                if 'P2534' in claims:
                    #print('Part of defining formula: ', entity.description)
                    output.put('Part of defining formula: '+ entity.description)

        except Exception as e:
            #print(qid, e)
            continue


meta = [(1,100,1), (101, 200, 2), (201, 300, 3), (301, 400, 4), (401, 500, 5)]


start = time()


processes = [Process(target=iterate_wikidata_pages, args=(m, output)) for m in meta]


print('processes about to start')
for p in processes:
    p.start()

print('all processes started')


for p in processes:
    p.join()

print('all processes joined')
end = time()


results = [output.get() for p in processes]
for r in results:
    print(r)


print('\n'*10)
print('ELAPSED TIME: ', end-start)"""




def iterate_wikidata_pages(r):
    #start, end, process_no = m

    #process = 'Process number: ' + str(process_no)
    client = Client()
    found_qids = {}
    #for qid in range(start, end):
    for qid in r:
        #print(process, qid)
        try:
            entity = client.get('Q' + str(qid), load=True)
            if 'claims' in entity.attributes:
                claims_dict = {'defining_formula':None,
                               'tex_string': None}
                claims = entity.attributes['claims']
                # Attribute P2534: defining formula
                if 'P2534' in claims:
                    defining_formula = claims['P2534'][0]['mainsnak']['datavalue']['value']
                    claims_dict['defining_formula'] = defining_formula
                # Attribbute P1993: TeX string
                if 'P1993' in claims:
                    tex_string = claims['P1993'][0]['mainsnak']['datavalue']['value']
                    claims_dict['tex_string'] = tex_string
                # contains at least one of these attributes
                # add the description and add to found_qids
                if claims_dict['defining_formula'] or claims_dict['tex_string']:
                    claims_dict['description'] = str(entity.description)
                    #print('in return ', qid, claims_dict)

                    found_qids[qid] = claims_dict

        except Exception as e:
            #print(qid, e)
            continue

    return found_qids



def calc_ranges(until, num_processes):
    k, m = divmod(len(until), num_processes)
    return (until[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_processes))



start = time()

num_processes = 2
ranges = calc_ranges(range(240,260), 2)
pool = Pool(processes=num_processes)
results = [pool.apply_async(iterate_wikidata_pages, args=(r,)) for r in ranges]
print('Processes started')

qids = {}
for p in results:
    d = p.get()
    qids.update(d)

print(qids)
end = time()
print('ELAPSED TIME: ', end-start)



"""start = time()

meta = [(1,100,1), (250, 380, 2)]
pool = Pool(processes=2)
results = [pool.apply_async(iterate_wikidata_pages, args=(m,)) for m in meta]
print('Processes started')

qids = {}
for p in results:
    d = p.get()
    qids.update(d)

print(qids)
end = time()
print('ELAPSED TIME: ', end-start)"""