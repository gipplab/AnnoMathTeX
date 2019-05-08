import os
import json
from ..config import recommendations_limit



class StaticWikidataHandler:
    """
    This class reads the extracted list of Wikidata identifiers and returns a dictionary of the results, with respect to
    the queried identifier. The queried identifier being an identifier clicked by the user through the frontend.
    """
    def __init__(self):
        self.evaluation_dict = self.read_file()


    def read_file(self):
        """
        Read the json file containing the static list of wikidata identifiers, that was extracted before.
        :return: The read file as a dictionary.
        """
        path = os.path.join(os.getcwd(), 'annomathtex', 'recommendation', 'evaluation_files', 'wikidata.json')
        with open(path, 'r') as infile:
            all_results = json.load(infile)
        return all_results


    def check_identifiers(self, symbol):
        """
        Return the entries of the static dictionary that match the symbol that was clicked by the user.
        :param symbol: The string of the symbol that was clicked by the user for annotation.
        :return: The corresponding matches from the dictionary of wikidata identifiers.
        """
        if symbol in self.evaluation_dict:
            return self.evaluation_dict[symbol][:recommendations_limit]
        return []
