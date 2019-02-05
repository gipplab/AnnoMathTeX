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
from nltk.tokenize import wordpunct_tokenize
from itertools import chain, groupby, product
import nltk
from string import punctuation


######### RAKE ##########
# https://github.com/csurfer/rake-nltk
from rake_nltk import Rake
from nltk.corpus import stopwords


class RakeIdentifier:
    #todo: add wikidata query check to see whether the found keywords are e.g. part of science

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
        rank_dict = {phrase:rank for (rank, phrase) in ranked_phrases_with_scores}
        return rank_dict

    def extract_identifiers(self, line_chunk, endline, cutoff):
        """
        loading the stopwords takes quite long I think
        :param line_chunk:
        :param endline:
        :param cutoff: minimum value for rank, in order for the word to be highlighted
        :return:
        """
        rank_dict = self.get_ranks(line_chunk)

        # All things which act as sentence breaks during keyword extraction.
        stopWords = set(stopwords.words('english'))

        to_ignore = set(chain(stopWords, punctuation))

        #this part is adapted from the rake_nltk source code, to get the same grouping of the sentences
        word_list = wordpunct_tokenize(line_chunk)
        groups = groupby(word_list, lambda x: x not in to_ignore)
        phrases = [tuple(group[1]) for group in groups]


        processed_phrases = []
        for t_phrase in phrases:
            phrase = ' '.join(w for w in t_phrase)
            rank = rank_dict[phrase.lower()] if phrase.lower() in rank_dict else 0.0
            processed_phrases.append(
                Word(str(uuid1()),
                     type='Word',
                     highlight='green' if rank > cutoff else 'black',
                     content=phrase,
                     endline=False,
                     named_entity=False,
                     wikidata_result=None)
            )

        if endline:
            processed_phrases[-1].endline = True


        return processed_phrases



########### Spacey ##############
import en_core_web_sm


class SpaceyIdentifier:
    """
    Right now uses named entities, maybe it would be better to use pos tags (e.g. PNOUN)
    """
    nlp = en_core_web_sm.load()
    test_text = "The case could escalate tensions between China and the US says Donald Trump."

    def extract_identifiers(self, line_chunk, endline):
        nlp_line_chunk = self.nlp(line_chunk)
        named_entities = set(str(ne) for ne in nlp_line_chunk.ents)


        words = [
            Word(str(uuid1()),
                 type='Word',
                 highlight='green' if str(w) in named_entities else 'black',
                 content=str(w),
                 endline=False,
                 named_entity=True if str(w) in named_entities else False,
                 wikidata_result=None)

            for w in nlp_line_chunk
        ]

        if endline:
            words[-1].endline = True


        return words





