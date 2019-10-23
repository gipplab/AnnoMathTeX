import os
import json





if __name__ == '__main__':

    with open(os.getcwd() + '/wikidata_identifiers.json', 'r') as infile:
        string = infile.read()
        all = json.loads(string)


    count = len(list(all.keys()))

    print(count)