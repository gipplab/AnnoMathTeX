from multiprocessing import Pool
from wikidata.client import Client
from time import time


"""
Multiprocessing to extract entities from wikidata -> construct dataset
"""

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
    #https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    k, m = divmod(len(until), num_processes)
    return (until[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_processes))


def testing(num_processes):
    print(num_processes, ' Processes running')
    start = time()

    ranges = calc_ranges(range(1, 5000), num_processes)
    pool = Pool(processes=num_processes)
    results = [pool.apply_async(iterate_wikidata_pages, args=(r,)) for r in ranges]

    qids = {}
    for p in results:
        d = p.get()
        qids.update(d)

    print(qids)
    end = time()
    print('ELAPSED TIME with ', num_processes, ' processes: ', end - start)



#############
#25 processes seems to be good
#############
