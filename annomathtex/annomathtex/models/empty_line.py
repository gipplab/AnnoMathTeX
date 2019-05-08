from .token import Token


class EmptyLine(Token):

    def __init__(self, unique_id, type='Emptyline', highlight=None, content=None, endline=True):
        """
        An empty line is treated like any other token, this enables relatively simple rendering of the file at the
        frontend of the project.

        :param unique_id: uuid.uuid1 object, converted to a string. Needed in template for rendering.
        :param type: String, "Word", "Identifier", "Formula", or "Endline". Needed for correct template rendering.
        :param highlight: String, colour, that the Identifier should be highlighted in. None if no highlight desired.
        :param content: String, The Identifier itself.
        :param endline: Boolean, needed for page rendering, true if token ends the line.
        """

        super().__init__(unique_id, type, highlight, content, endline)

