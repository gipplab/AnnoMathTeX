import os
import json
from ..config import recommendations_limit



class StaticWikidataHandler:

    def __init__(self):
        self.evaluation_dict = self.read_file()


    def read_file(self):
        path = os.getcwd() + '/annomathtex/recommendation/evaluation_files/wikidata.json'
        with open(path, 'r') as infile:
            all_results = json.load(infile)
        return all_results



    def check_identifiers(self, symbol):
        if symbol in self.evaluation_dict:
            return self.evaluation_dict[symbol][:recommendations_limit]
        return []
