from django.db import models
import json

class File(models.Model):

    def __init__(self, processed_lines, __linked_words__, __linked_math_symbols__, file_name, existing_annotations=None):
        """

        :param processed_lines: Each processed line consists of one or mulitple chunks. A chunk
        is either a math environment or not. A math environment chunk consists of identifiers.
        A non-math environment chunk consists of words.
        :param __linked_words__: Dictionary of the identical words in the document (necessary for global annotations).
        :param __linked_math_symbols__: Dictionary of the identical math symbols (identifiers, formulae) in the
        document (necessary for global annotations).
        :param file_name: The name of the file that is being worked on by the user.
        :param existing_annotations: If the user worked on this file before, any annotations he made are stored in this
        variable.
        """
        self.body = processed_lines
        linked_words, linked_math_symbols = map(
            self.handle_linked_tokens, [__linked_words__, __linked_math_symbols__]
        )
        self.linked_words = json.dumps({'linkedWords': linked_words})
        self.linked_math_symbols = json.dumps({'linkedMathSymbols': linked_math_symbols})
        self.file_name = file_name
        self.existing_annotations = json.dumps({'existingAnnotations': existing_annotations})


    def handle_linked_tokens(self, links_dict):
        """
        Remove those items that exist only once in the document.
        No point in keeping them, because the point of the linked dictionaries is to only have to annotate
        an item once for the entire document.
        :param links_dict: Dictionary of words or math symbols.
        :return: Dictionary of only words or math symbols that appear multiple times in the document.
        """
        for key in list(links_dict.keys()):
            if len(links_dict[key]) <= 1:
                del links_dict[key]
        return links_dict

