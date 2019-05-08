from .token import Token


class Identifier(Token):

    def __init__(
        self,
        unique_id,
        type,
        highlight,
        content,
        endline,
        math_env
    ):
        """
        Constructor of superclass Token is called for highlight and content

        :param unique_id: uuid.uuid1 object, converted to a string. Needed in template for rendering.
        :param type: String, "Word", "Identifier", "Formula", or "Endline". Needed for correct template rendering.
        :param highlight: String, colour, that the Identifier should be highlighted in. None if no highlight desired.
        :param content: String, The Identifier itself.
        :param endline: Boolean, needed for page rendering, true if token ends the line.
        """
        super().__init__(
            unique_id,
            type,
            highlight,
            content,
            endline,
            math_env = math_env
        )
