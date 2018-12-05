from .token import Token


class Identifier(Token):
    #todo: method: find wikidata quid

    def __init__(self, highlight, content, endline, qid):
        """
        Constructor of superclass Token is called for highlight and content

        :param highlight: String, colour, that the Identifier should be highlighted in. None if no highlight desired.
        :param content: String, The Identifier itself.
        :param endline: Boolean, needed for page rendering
        :param qid: String, the Wikidata Quid corresponding to the identifier.
        """
        super().__init__(highlight, content, endline)
        self.qid = qid

    def get_type(self):
        """
        Get the name of the current class.
        :return: Name of class.
        """
        return self.__name__

    def get_highlight(self):
        """
        Get the highlight value for the Word.
        :return: Colour of highlighting, None if no highlighting.
        """
        return self.highlight

    def get_content(self):
        """
        Get the word itself.
        :return: String of word
        """
        return self.content

    def get_endline(self):
        """
        Get the boolean value.
        :return: endline, true or false
        """
        return self.endline

    def get_qid(self):
        """
        Get the Wikidata Quid for the identifier
        :return: Wikidata Quid
        """
        return self.qid
