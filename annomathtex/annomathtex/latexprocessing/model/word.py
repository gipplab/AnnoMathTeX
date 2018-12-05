"""class Word:

    def __init__(self, token, highlight=False):
        self.content = token
        self.highlight = highlight"""


from .token import Token

"""
This class inherits from Token. Every word in the LaTeX file is a Word. 
"""

class Word(Token):
    #todo: add colouring for named entity is this class

    def __init__(self, highlight, content, endline, named_entity):
        """
        Constructor of superclass Token is called for highlight and content

        :param highlight: String, colour, that the Word should be highlighted in. None if no highlight desired.
        :param content: String, The Word itself.
        :param endline: Boolean, needed for page rendering
        :param named_entity: Boolean, whether the Word is a named entity.
        """
        super().__init__(highlight, content, endline)
        self.named_entity = named_entity

    def get_type(self):
        """
        Get the name of the current class.
        :return: Name of class.
        """
        return self.__class__.__name__

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

    def get_named_entity(self):
        """
        Get a boolean stating whether Word is a named entity or not.
        :return: Boolean, named entity or not.
        """
        return self.named_entity
