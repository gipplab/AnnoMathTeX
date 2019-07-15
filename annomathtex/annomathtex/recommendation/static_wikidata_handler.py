import os
import json
from ..config import recommendations_limit
from ..settings.common import PROJECT_ROOT
from fuzzywuzzy import fuzz
from operator import itemgetter

#recommendations_limit = 10
#PROJECT_ROOT = ''

#todo: commit static wikidata files to data repo and get from there

class StaticWikidataHandler:
    """
    This class reads the extracted list of Wikidata identifiers and returns a dictionary of the results, with respect to
    the queried identifier. The queried identifier being an identifier clicked by the user through the frontend.
    """


    def read_identifier_file(self):
        """
        Read the json file containing the static list of wikidata identifiers, that was extracted before.
        :return: The read file as a dictionary.
        """
        path = os.path.join(PROJECT_ROOT, 'annomathtex', 'recommendation', 'evaluation_files', 'wikidata.json')
        with open(path, 'r') as infile:
            all_results = json.load(infile)
        return all_results


    def read_formula_file(self):
        path = os.path.join(PROJECT_ROOT, 'annomathtex', 'recommendation', 'evaluation_files', 'wikidata_formulae.json')
        with open(path, 'r') as infile:
            all_results = json.load(infile)
        return all_results


    def read_formula_file_test(self):
        path = os.path.join(os.getcwd(), 'evaluation_files', 'wikidata_formulae.json')
        with open(path, 'r') as infile:
            all_results = json.load(infile)
        return all_results


    def toLowerCase(self, dict_list):
        for d in dict_list:
            d['name'] = d['name'].lower()
        return dict_list


    def check_identifiers(self, symbol):
        """
        Return the entries of the static dictionary that match the symbol that was clicked by the user.
        :param symbol: The string of the symbol that was clicked by the user for annotation.
        :return: The corresponding matches from the dictionary of wikidata identifiers.
        """
        identifier_file = self.read_identifier_file()
        if symbol in identifier_file:
            return self.toLowerCase(self.read_identifier_file()[symbol][:recommendations_limit])
        return []


    def extract_identifiers_from_formula(self, annotations, formula_string):
        #todo: include local
        annotations = annotations['global']
        identfifiers = []
        for id_or_formula in annotations:
            if 'mathEnv' in annotations[id_or_formula] and annotations[id_or_formula]['mathEnv'] == formula_string:
                identfifiers.append(id_or_formula)
                identfifiers.append(annotations[id_or_formula]['name'])

        return identfifiers


    def check_formulae(self, formula_string, annotations, threshold_string=65, threshold_identifers = 1):
        results_string = []
        results_identifiers = []
        formula_dict = self.read_formula_file()
        identifiers = self.extract_identifiers_from_formula(annotations, formula_string)
        for formula_name in formula_dict:
            formula = formula_dict[formula_name]
            tex_string = formula['formula']



            score_string = fuzz.token_sort_ratio(formula_string, tex_string)
            if score_string >= threshold_string:
                results_string.append(({'name':formula_name}, score_string))

            formula_identifiers = formula['identifiers']['names']
            formula_quantity_symbols = formula['identifiers']['strings']
            score_identifers = len(
                                   list(
                                        set(identifiers).intersection(formula_quantity_symbols+formula_identifiers)
                                   )
            )
            if score_identifers >= threshold_identifers:
                results_identifiers.append(({'name':formula_name}, score_identifers))


        if len(results_string)>0:
            results_string = [r[0] for r in sorted(results_string, key=itemgetter(1))]
            #results_string = results_string.sort(reverse=True)[:10]
        if len(results_identifiers)>0:
            #results_identifiers = results_identifiers.sort(reverse=True)[:10]
            results_identifiers = [r[0] for r in sorted(results_identifiers, key=itemgetter(1))]

        return results_string, results_identifiers






if __name__ == '__main__':
    s = StaticWikidataHandler()
    #f = s.read_formula_file_test()
    #for i in f:
    #    print(i)
    s, i = s.check_formulae('E = m c^2', ['energy', 'mass', 'speed of light', 'E', 'm', 'c'])
    print(s)
    print(i)

