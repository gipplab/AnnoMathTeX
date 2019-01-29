"""
Retrieve the correct identifier from the surrounding text

Ideas:
Use Spacey to find QUANTITY attributes
https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da


Use python keyword extraction algorithms
    - RAKE https://www.airpair.com/nlp/keyword-extraction-tutorial


Train word2vec on test dataset
    - use word2vec and GloVe to determine the similarity between words of surrounding text and the identifier
https://textminingonline.com/training-word2vec-model-on-english-wikipedia-by-gensim#comment-138807
https://textminingonline.com/getting-started-with-word2vec-and-glove-in-python

"""
from .model.word import Word
from uuid import uuid1
import nltk


######### RAKE ##########
"""
The phrases are generated in the method _generate_phrases()
should try to access that
"""


# https://github.com/csurfer/rake-nltk
from rake_nltk import Rake


class RakeIdentifier:

    r = Rake()
    test_text = "The case could escalate tensions between China and the US."

    def get_ranks(self, line_chunk):
        """
        Calculate the ranks for phrases within the line
        :param line_chunk:
        :return:
        """
        self.r.extract_keywords_from_text(line_chunk)

        #phrases sorted highest to lowest
        ranked_phrases_with_scores = self.r.get_ranked_phrases_with_scores()

        rank_dict = {}
        rank_string = ''
        for rank, phrase in ranked_phrases_with_scores:
            rank_dict[phrase] = rank
            rank_string += phrase
        #rank_dict = {phrase:rank for (rank, phrase) in ranked_phrases_with_scores}

        #contains the phrases that have been ranked by RAKE
        #can then check which phrases are not contained, and assign 0.0 to them
        #rank_string = '-'.join(rank_dict[k] for k in rank_dict)


        #words not returned by ranking (too low score)
        #left_over = {word:0 for word in nltk.word_tokenize(line_chunk) if word not in rank_string}
        print([w for w in nltk.word_tokenize(line_chunk)])
        #concatenate the 2 dictionaries
        #return dict(rank_dict, **left_over)
        return rank_dict

    def extract_identifiers(self, line_chunk, endline, cutoff):
        """

        :param line_chunk:
        :param endline:
        :param cutoff: minimum value for rank, in order for the word to be highlighted
        :return:
        """
        rank_dict = self.get_ranks(line_chunk)
        print(rank_dict)

        #print(len(rank_dict.keys()), print(len(nltk.word_tokenize(line_chunk))))
        #print(nltk.word_tokenize(line_chunk))
        #for w in nltk.word_tokenize(line_chunk):
        #    print(w, rank_dict[w])

        #print('\n##############\n')

        """for word in nltk.word_tokenize(line_chunk):
            if rank_dict[word] > cutoff:
                print(True, rank_dict[word], word)
            else:
                print(False, rank_dict[word], word)"""

        words = [
            Word(str(uuid1()),
                 type='Word',
                 highlight='green' if rank_dict[word]>cutoff else 'black',
                 content=word,
                 endline=False,
                 named_entity=False,
                 wikidata_result=None)
            for word in nltk.word_tokenize(line_chunk)
        ]

        if endline:
            words[-1].endline = True

        #for w in nltk.word_tokenize(line_chunk):
        #    print(w)

        return words

