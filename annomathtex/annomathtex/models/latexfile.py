from django.db import models
import json



class LaTeXFile(models.Model):

    def __init__(self, processed_lines, __linked_words__, __linked_math_symbols__, file_name, existing_annotations=None):
        """

        :param processed_lines: each processed line consists of one or mulitple chunks. A chunk
        is either a math environment or not. A math environment chunk consists of identifiers.
        A non-math environment chunk consists of words.
        """
        self.body = processed_lines
        linked_words, linked_math_symbols = map(
            self.handle_linked_tokens, [__linked_words__, __linked_math_symbols__]
        )
        #linked_words['Sun'] = ["TESTID"] + linked_words['Sun']
        self.linked_words = json.dumps({'linkedWords': linked_words})
        self.linked_math_symbols = json.dumps({'linkedMathSymbols': linked_math_symbols})
        self.file_name = file_name
        self.existing_annotations = json.dumps({'existingAnnotations': existing_annotations})

        #for k in linked_math_symbols:
        #    print(k, len(linked_math_symbols[k]), len(list(set(linked_math_symbols[k]))))

        #for k in linked_words:
        #    print(k, len(linked_words[k]), len(list(set(linked_words[k]))))


        #self.test_val = json.dumps({'test': [linked_words]})


    def handle_linked_tokens(self, links_dict):
        """
        Remove those items that exist only once in the document.
        No point in keeping them, because the point of the linked dictionaries is to only have to annotate
        an item once for the entire document.
        :param links_dict:
        :return:
        """
        for key in list(links_dict.keys()):
            if len(links_dict[key]) <= 1:
                del links_dict[key]
        return links_dict

