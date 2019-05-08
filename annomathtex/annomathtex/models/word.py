from .token import Token

class Word(Token):

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
