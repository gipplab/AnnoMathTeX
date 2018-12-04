from abc import ABCMeta, abstractmethod

"""
Each word/identifier in a tex document is a token. A token must be one of those 2.
Punctuation are excluded.
"""

class Token(object, metaclass=ABCMeta):

    def __init__(self, highlight, content):
        """
        :param highlight: String, color, that the Token should be highlighted in. None if no highlight desired.
        :param content: String, The Word/Identifier itself.
        """
        self.highlight = highlight
        self.content = content

    @abstractmethod
    def get_type(self):
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def get_highlight(self):
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def get_content(self):
        raise NotImplementedError('must be impplemented')
