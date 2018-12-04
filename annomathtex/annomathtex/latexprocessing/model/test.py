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
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def get_highlight(self):
        raise NotImplementedError('must be impplemented')

    @abstractmethod
    def get_content(self):
        raise NotImplementedError('must be impplemented')



class Word(Token):

    def __init__(self, highlight, content, named_entity):
        super().__init__(highlight, content)
        self.named_entity = named_entity

    def get_type(self):
        return self.__class__.__name__

    def get_highlight(self):
        return self.highlight

    def get_content(self):
        return self.content

    def get_named_entity(self):
        return self.named_entity



w = Word(1, 2, 3, 4)


print(w.get_type())
print(w.get_highlight())
print(w.get_content())
print(w.get_named_entity())
