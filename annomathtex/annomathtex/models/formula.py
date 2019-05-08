from .token import Token


class Formula(Token):

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

        A formula object contains the entire math evironment. The user can access it by clicking the delimiter of the
        formula (e.g. '$').

        :param unique_id: uuid.uuid1 object, converted to a string. Needed in template for rendering.
        :param type: String, "Word", "Identifier", "Formula", or "Endline". Needed for correct template rendering.
        :param highlight: String, colour, that the Identifier should be highlighted in. None if no highlight desired.
        :param content: String, The Identifier itself.
        :param endline: Boolean, needed for page rendering, true if token ends the line.
        :param math_env: The entire math environment. The content of the Formula object is the delimiter (e.g. '$') but
                         the content is the entire string.
        """
        super().__init__(
            unique_id,
            type,
            highlight,
            content,
            endline,
            math_env
        )
