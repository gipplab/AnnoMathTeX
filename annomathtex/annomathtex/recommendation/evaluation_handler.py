# Not used atm

from abc import ABCMeta, abstractmethod


class EvaluationHandler(object, metaclass=ABCMeta):
    """
    Abstract base class for classes that need to handle identifier look up in evaluation files.
        - WikipediaEvaluationHandler
        - ArXivEvaluationHandler
    """

    def __init__(self, path_to_evaluation_file):
        self.file = self.read_file(path_to_evaluation_file)

    @abstractmethod
    def read_file(self, path_to_evaluation_file):
        """
        Read the file that contains the evaluation list.
        :return: The loaded and read file (as string).
        """
        raise NotImplementedError('Method read_file must be implemented')

    @abstractmethod
    def create_item_dict(self):
        """
        Create a dictionary of the evaluation list.
        :return: The created dictionary
        """
        raise NotImplementedError('Method create_item_dict must be implemented')


    def check_identifiers(self, symbol):
        pass
