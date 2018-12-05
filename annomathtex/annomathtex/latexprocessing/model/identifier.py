from .token import Token


class Identifier(Token):
    #todo: method: find wikidata quid

    def __init__(self, type, highlight, content, endline, qid):
        """
        Constructor of superclass Token is called for highlight and content

        :param type: String, "Word" or "Identifier". Needed for correct template rendering
        :param highlight: String, colour, that the Identifier should be highlighted in. None if no highlight desired.
        :param content: String, The Identifier itself.
        :param endline: Boolean, needed for page rendering
        :param qid: String, the Wikidata Quid corresponding to the identifier.
        """
        super().__init__(type, highlight, content, endline)
        self.qid = qid

    def get_type(self):
        """
        Get the name of the current class.
        :return: Name of class.
        """
        return self.type

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

    def set_endline(self, new_endline_val):
        """
        set the endline value
        :param new_endline_val:
        :return: None
        """
        self.endline = new_endline_val
