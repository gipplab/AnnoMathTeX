import os


class ArXivEvaluationListHandler:
    """
    This class reads the extracted list of arXiv identifiers and returns a dictionary of the results, with respect to
    the queried identifier. The queried identifier being an identifier clicked by the user through the frontend.
    """
    def __init__(self):
        self.evaluation_file = self.read_file()
        self.evaluation_dict = self.create_item_dict()

    def read_file(self):
        """
        Read the file containing the extacted arXiv identifiers.
        :return: The read file as a string, with some unnecessary characters removed.
        """
        path = os.path.join(os.getcwd(), 'annomathtex', 'recommendation', 'evaluation_files', 'Evaluation_list_all.rtf')
        with open(path, 'r') as f:
            file = f.read()
        file = file.replace('\par', '\n')
        return file.split('\n\n\n\n')[1:]

    def create_item_dict(self):
        """
        Create a dictionary of the file that was parsed by the method read_file().
        :return: The dictionary that was created.
        """
        item_dict = {}
        for item in self.evaluation_file:
            item_parts = item.split('\n\n')
            if len(item_parts) >= 11:
                if len(item_parts) == 12:
                    item_parts = item_parts[:-1]
                identifier = item_parts[0].replace('\\', '')
                item_dict[identifier] = list(
                    map(
                        lambda x: {
                            'name': x.split()[0][:-1]
                        },
                        item_parts[1:]
                    )
                )
        return item_dict


    def check_identifiers(self, symbol):
        """
        Return the entries of the created dictionary that match the symbol that was clicked by the user.
        :param symbol: The string of the symbol that was clicked by the user for annotation.
        :return: The corresponding matches from the dictionary of arXiv identifiers.
        """
        if symbol in self.evaluation_dict:
            return self.evaluation_dict[symbol]
        return []

