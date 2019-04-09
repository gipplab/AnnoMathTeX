from .token import Token

class Word(Token):
    #todo: add colouring for named entity is this class
    #todo: differentiate between named entity and NNS

    def __init__(
        self,
        unique_id,
        type,
        highlight,
        content,
        endline,
        named_entity
    ):
        """
        This class inherits from Token. Every word in the LaTeX file is a Word.

        :param unique_id: uuid.uuid1 object, converted to a string. Needed in template for rendering.
        :param type: String, "Word", "Identifier", "Formula", or "Endline". Needed for correct template rendering.
        :param highlight: String, colour, that the Word should be highlighted in. None if no highlight desired.
        :param content: String, The Word itself.
        :param endline: Boolean, needed for page rendering, true if token ends the line.
        :param named_entity: Boolean, needed for highlighting.
        """
        super().__init__(
            unique_id,
            type,
            highlight,
            content,
            endline,
        )
        self.named_entity = named_entity

    def get_unique_id(self):
        """
        Get the unique id of the word
        :return: String of unique id
        """
        return self.unique_id

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

    def get_named_entity(self):
        """
        Get a boolean stating whether Word is a named entity or not.
        :return: Boolean, named entity or not.
        """
        return self.named_entity

    def set_endline(self, new_endline_val):
        """
        set the endline value
        :param new_endline_val:
        :return: None
        """
        self.endline = new_endline_val
