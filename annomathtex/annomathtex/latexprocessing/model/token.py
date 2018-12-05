from abc import ABCMeta, abstractmethod

"""
Each word/identifier in a tex document is a token. A token must be one of those 2.
Punctuation are excluded.
"""

class Token(object, metaclass=ABCMeta):

    def __init__(self, type, highlight, content, endline):
        """
        :param type: String, "Word" or "Identifier". Needed for correct template rendering
        :param highlight: String, color, that the Token should be highlighted in. None if no highlight desired.
        :param content: String, The Word/Identifier itself.
        :param endline: Boolean, needed for page rendering
        """
        self.highlight = highlight
        self.content = content
        self.endline = endline
        self.type = type

    @abstractmethod
    def get_type(self):
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def get_highlight(self):
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def get_content(self):
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def get_endline(self):
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def set_endline(self, new_endline_val):
        raise NotImplementedError('must be impplemented')
