import os
import json
from ..config import recommendations_limit


class WikipediaEvaluationListHandler:

    def __init__(self):
        self.identifier_dict = self.read_file()


    def read_file(self):
        path = os.getcwd() + '/annomathtex/recommendation/evaluation_files/wikipedia_list.json'
        with open(path, 'r') as json_file:
            identifier_dict = json.load(json_file)

        #print(identifier_dict)

        return identifier_dict


    def check_identifiers(self, symbol):
        if symbol in self.identifier_dict:
            # limit to the specified number few entries (in config file)
            #print(self.identifier_dict[symbol])
            identifier_dict_symbol = self.identifier_dict[symbol]
            new_d = []
            found_descriptions = []
            for d in identifier_dict_symbol:
                if d['description'] not in found_descriptions:
                    new_d.append(d)
                    found_descriptions.append(d['description'])
            return new_d[:recommendations_limit]
            #return self.identifier_dict[symbol][:recommendations_limit]
        return None

