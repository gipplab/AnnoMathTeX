import os
import numpy as np
import json
import csv

path = "annotations"


header = "Identifer,Name,Occurences"

rows = []
for file in os.listdir(path)[1:]:
    if file.endswith('txt'):
        with open(os.path.join(path, file), 'r') as f:
            json_file = json.loads(f.read())


            if 'global' in json_file:
                g = json_file['global']

                for identifier in g:
                    name = g[identifier]['name']
                    if 'uniqueIDs' in g[identifier]:
                        num_ids = len(g[identifier]['uniqueIDs'])
                    else:
                        num_ids = 0
                    row = [identifier, name, num_ids]
                    rows.append(row)

            if 'local' in json_file:
                l = json_file['local']
                for identifier in l:
                    id = list(l[identifier].keys())[0]
                    name = l[identifier][id]['name']
                    row = [identifier, name, 1]
                    rows.append(row)



with open(os.path.join(os.getcwd(), 'annotation_statistic.csv'), 'w') as g:
    csv_writer = csv.writer(g, delimiter=',')
    csv_writer.writerows(rows)


