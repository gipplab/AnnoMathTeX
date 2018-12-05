class LaTeXFile:

    def __init__(self, processed_lines):
        """

        :param processed_lines: each processed line consists of one or mulitple chunks. A chunk
        is either a math environment or not. A math environment chunk consists of identifiers.
        A non-math environment chunk consists of words.
        """
        self.body = processed_lines

