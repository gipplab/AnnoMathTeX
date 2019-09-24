from itertools import zip_longest
from ...config import *

from ...recommendation.ne_sparql import NESparql

####################################################################################
####################################################################################
######################################not used #####################################
####################################################################################
####################################################################################

class ConcatenatedRecommendationsHandler:
    """
    Concatenate the recommendations from the various sources and show them in the first column.
    :param wikidata_results: The results that were obtained from querying the wikidata query service API.
    :param arXiv_evaluation_items: The results that were obtained from checking string matches of the character
                                   in the evaluation list from ArXiv. Only for identifiers.
    :param wikipedia_evaluation_items: The results that were obtained from checking string matches of the character
                                       in the evaluation list from Wikipedia. Only for identifiers.
    :param word_window: The named entities (as found by the tagger) that surround the identifier/formula within
                        the text.
    :return: A list of unique results where as long as the source contains more results the order goes Wikidata,
             ArXiv, Wikipedia, Word Window.
    """


    def get_recommendations(self, type, wikidata_results, arXiv_evaluation_items,
                                         wikipedia_evaluation_items, word_window):

        all_recommendations = zip_longest(
                                              wikidata_results,
                                              arXiv_evaluation_items,
                                              wikipedia_evaluation_items,
                                              word_window,
                                              fillvalue={'name':'__FILLVALUE__'}
                                          )
        count = 0
        seen = ['__FILLVALUE__']
        concatenated_recommendations = []
        for zip_r in all_recommendations:
            #print(zip_r)
            for r in zip_r:
                if count == recommendations_limit: break
                if r['name'] not in seen:
                    if 'qid' not in r:
                        results = NESparql().concatenated_column_search(r['name'])
                        r = results[0] if results else r
                    concatenated_recommendations.append(r)
                    seen.append(r['name'])
                    count += 1


        return concatenated_recommendations
