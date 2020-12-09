import os, csv, re


def get_file_list(location):
    return [f for f in os.listdir(location) if f.endswith('.csv')]


def get_qids(filename):
    pat_q = re.compile('\(Q(\d+)\)$')
    result = dict()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            content = row['Identifier / Formula']
            m = pat_q.search(row['Name'])
            if m and content.__contains__('='):
                result[content] = m.group(1)
        return result
