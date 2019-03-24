import os
import json
from ..config import recommendations_limit


class WikipediaEvaluationListHandler:

    def __init__(self):
        self.identifier_dict = self.read_file()


    def read_file(self):
        path = os.getcwd() + '/annomathtex/latexprocessing/evaluation_files/wikipedia_list.json'
        with open(path, 'r') as json_file:
            identifier_dict = json.load(json_file)

        #print(identifier_dict)

        return identifier_dict


    def check_identifiers(self, symbol):
        if symbol in self.identifier_dict:
            # limit to the specified number few entries (in config file)
            return self.identifier_dict[symbol][:recommendations_limit]
        return None





class ArXivEvaluationListHandler:

    def __init__(self):
        self.evaluation_file = self.read_file()
        self.evaluation_dict = self.create_item_dict()
        #print(self.evaluation_dict)

    def read_file(self):
        path = os.getcwd() + '/annomathtex/latexprocessing/evaluation_files/Evaluation_list_all.rtf'
        with open(path, 'r') as f:
            file = f.read()

        file = file.replace('\par', '\n')

        return file.split('\n\n\n\n')[1:]



    def create_item_dict(self):

        #print(file)

        item_dict = {}
        for item in self.evaluation_file:
            item_parts = item.split('\n\n')
            if len(item_parts) >= 11:
                if len(item_parts) == 12:
                    item_parts = item_parts[:-1]
                #print(item_parts)
                identifier = item_parts[0].replace('\\', '')
                item_dict[identifier] = list(
                    map(
                        #lambda x: (x.split()[0][:-1], x.split()[1]), item_parts[1:]
                        lambda x: {'name': x.split()[0][:-1], 'value': x.split()[1]}, item_parts[1:]
                    )
                )
                #item_dict[item_parts[0]] = [tuple(x[:-1] for x in i.split()) for i in item_parts[1:]]
                #identifier = item_parts

        #print(item_dict)
        return item_dict


    def check_identifiers(self, symbol):
        if symbol in self.evaluation_dict:
            # limit to the specified number few entries (in config file)
            return self.evaluation_dict[symbol][:recommendations_limit]
        return None



#item_dict = create_item_dict()
#print(item_dict)
#for k in item_dict:
#    print(k, item_dict[k])

