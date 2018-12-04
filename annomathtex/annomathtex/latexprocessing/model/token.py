from abc import ABCMeta, abstractmethod

"""
Each word/identifier in a tex document is a token. A token must be one of those 2.
"""

class Token(object, metaclass=ABCMeta):

    def __init__(self, type, highlight, content):
        self.type = type
        self.highlight = highlight
        self.content = content

    @abstractmethod
    def get_type(self):
        return self.type

    def get_highlight(self):
        return self.highlight

    def get_content(self):
        return self.content
