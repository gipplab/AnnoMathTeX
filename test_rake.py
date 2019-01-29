from nltk.tokenize import wordpunct_tokenize
from itertools import chain, groupby, product

test_text = "The case could escalate tensions between China and the US."

to_ignore = ['the', 'between', 'and']



def generate_phrases(sentences):
    phrase_list = set()
    # Create contender phrases from sentences.
    for sentence in sentences:
        word_list = [word.lower() for word in wordpunct_tokenize(sentence)]
        phrase_list.update(get_phrase_list(word_list))

    return phrase_list

def get_phrase_list(word_list):
    groups = groupby(word_list, lambda x: x not in to_ignore)
    g = [tuple(group[1]) for group in groups]
    print(g)
    #filters out stop words
    phrases = [tuple(group[1]) for group in groups if group[0]]
    #print(phrases)
    return list(
        filter(
            lambda x: 1 <= len(x) <= 100000, phrases
        )
    )


generate_phrases([test_text])