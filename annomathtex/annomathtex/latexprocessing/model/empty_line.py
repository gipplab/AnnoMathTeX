from .token import Token


"""
Needed to treat empty lines
"""

class EmptyLine(Token):

    def __init__(self, type='Emptyline', highlight=None, content=None, endline=True):
        """
        Constructor of superclass Token is called for highlight and content

        :param type: String, "Word","Identifier" or "Emptyline". Needed for correct template rendering
        :param highlight: String, colour, that the Identifier should be highlighted in. None if no highlight desired.
        :param content: String, The Identifier itself.
        :param endline: Boolean, needed for page rendering
        """
        super().__init__(type, highlight, content, endline)

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

    def set_endline(self, new_endline_val):
        """
        set the endline value
        :param new_endline_val:
        :return: None
        """
        self.endline = new_endline_val
